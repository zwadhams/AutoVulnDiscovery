import argparse
from z3 import *
import tree_sitter_c as tsc
from tree_sitter import Language, Parser
import os

# to do notes from hw :
#   ignore print f
#   when reaching return 1; save symbolic state add this to the constraints for solver
#   each branch should create two symbolic states, mark with SAT or UnSAT
#   fix handle declaration


C_LANG = Language(tsc.language())
parser = Parser(C_LANG)


# solver = Solver()


# Example path: Assignment3\test_program.c
def read_c_code_from_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def print_tree(node, indent=""):
    hold = f"{indent}{node.type} "  # [{node.start_point}, {node.end_point}]
    print(hold)
    for child in node.children:
        print_tree(child, indent + "  ")
    return


class SymbolicExecutor:
    def __init__(self):
        # Initializes the Z3 solver for constraint checking
        # self.solver = Solver()
        # Dictionary to store function nodes, allowing for function calls
        self.functions = {}
        # Maps variable names to their SymbolicVariable instances
        self.mapping = {}
        # Counter for generating unique variable identifiers
        self.counter = 0
        self.condition = {}
        self.current_path_condition = BoolVal(True)
        # Stack to save and restore states for branching
        self.saved_states = []
        # Counters to track feasible and infeasible paths
        self.SAT = 0
        self.UnSAT = 0
        # Counter for paths that meet the target condition `return 1;`
        self.targetReached = 0

    def save_state(self):
        # Saves the current state by storing the path condition,
        # variable mappings, and counter in the saved states stack.
        state = {
            "conditions": self.condition,
            "mapping": self.mapping.copy(),
            "counter": self.counter
        }
        self.saved_states.append(state)
        print("State saved.")

    def restore_state(self):
        # Restores the last saved state, including the path condition,
        # variable mappings, and counter.
        if self.saved_states:
            state = self.saved_states.pop()
            self.condition = state["conditions"]
            self.mapping = state["mapping"]
            self.counter = state["counter"]
            print("State restored.")
        else:
            print("No saved state to restore.")

    def execute(self, root_node, function):
        # Main entry point to execute the symbolic interpreter on a function
        # Parses all functions from the root node and then begins traversing
        # the specified function node
        self.Find_Functions(root_node)
        node = self.functions[function]
        self.traverse_node(node)
        # Outputs results on paths after execution
        print("Number of infeasible states:", self.UnSAT)
        print("Number of feasible states:", self.SAT)
        print("Number of Target reached:", self.targetReached)

    def Find_Functions(self, node):
        # Recursive function to locate and store all function definitions
        # within the code tree. Assumes function name is the first child node.
        if node.type == 'function_definition':
            declarator_node = node.child_by_field_name('declarator')
            function_name_node = declarator_node.children[0]
            function_name = function_name_node.text.decode('utf-8')
            self.functions[function_name] = node
            print("Function found:", function_name)
        elif node.type == 'declaration':
            # Processes variable declarations
            self.handle_declaration(node)
        for child in node.children:
            self.Find_Functions(child)

    # Example helper functions for increment and decrement
    def handle_increment(self, var_name):
        # Assuming self.symbolic_state holds the current symbolic variable states
        if var_name in self.mapping:
            self.condition[self.mapping[var_name]] = self.mapping[var_name] + 1  # Increment symbolic state
        else:
            raise KeyError(f"Variable {var_name} not found in symbolic state.")

    def handle_decrement(self, var_name):
        if var_name in self.mapping:
            self.condition[self.mapping[var_name]] = self.mapping[var_name] - 1  # Decrement symbolic state
        else:
            raise KeyError(f"Variable {var_name} not found in symbolic state.")

    def traverse_node(self, node):
        # Traverses each node type in the function body and delegates handling
        # of specific node types to helper methods based on functionality
        if node is None:
            return
        elif node.type =='update_expression':
            # Handle increment (++) and decrement (--) expressions
            expression_text = node.text.decode('utf-8').strip()  # Get the expression text
            if expression_text.endswith('++'):
                var_name = expression_text[:-2].strip()
                self.handle_increment(var_name)
            elif expression_text.endswith('--'):
                var_name = expression_text[:-2].strip()
                self.handle_decrement(var_name)

        elif node.type == 'call_expression':
            # Handles function calls if the called function is in the stored dictionary
            function_name = node.children[0].text.decode('utf-8')
            if function_name in self.functions:
                self.traverse_node(self.functions[function_name])
        elif node.type == 'declaration':
            # Declaration node for new variable declarations
            self.handle_declaration(node)
        elif node.type == 'assignment_expression':
            # Assignment node for updating variable values
            self.handle_assignment(node)
        elif node.type == 'if_statement':
            # Conditional branching
            self.handle_if_statement(node)
        # just trying to make sure if works then we will go to this.
        elif node.type == 'while_statement':
        #     # Loops, handled similarly to conditionals but with iterative feasibility checking
            self.handle_while_statement(node)
        # elif node.type == 'return_statement':
        #     # Handles return statements, with specific handling for the target `return 1`
        #     self.handle_return(node)
        else:
            pass

        # Recursively traverses child nodes
        for child in node.children:
            self.traverse_node(child)

    def handle_declaration(self, node):
        # Just getting the values
        declarator_node = node.child_by_field_name('declarator')

        # Generates a unique identifier for the symbolic variable
        unique_id = f'X{self.counter}'
        self.counter += 1  # add to counter so ids are unique.

        if not declarator_node.children:
            # create a mapping for example int x: x->X1
            self.mapping[declarator_node.text.decode()] = unique_id
            print(f"Declared variable {declarator_node.text.decode()} mapped to {unique_id}")
        else:
            # Extracts the variable name
            var_name = declarator_node.children[0].text.decode()
            # add the values to the map and conditions.
            self.mapping[var_name] = unique_id
            self.condition[unique_id] = declarator_node

            print(f"Declared variable {var_name} mapped to {unique_id} with value: {declarator_node.text.decode()}")

    def handle_assignment(self, node):
        # Updates a variable with a new condition
        var_name = node.child_by_field_name('left').text.decode()
        expr = node.child_by_field_name('right')
        # value = self.evaluate_expression(expr)
        if var_name in self.mapping:
            symbolic_var = self.mapping[var_name]
            self.condition[symbolic_var] = node  # should never
        print(f"Assigned {var_name} = {node} ")

    def handle_if_statement(self, node):
        # Handles if statements by creating branches for true and false conditions
        condition_node = node.child_by_field_name('condition')
        true_branch = node.child_by_field_name('consequence')
        false_branch = node.child_by_field_name('alternative')

        new_condition = condition_node.children[1]
        # True branch feasibility check and traversal if feasible
        if self.check_feasibility(new_condition):

            self.save_state()  # save the state and then traverse this branch
            self.traverse_node(true_branch)
            self.SAT += 1  # satisfiable condition
            self.restore_state()  # go back to the previous state and try the other side of the condition

        else:
            self.save_state()
            self.traverse_node(false_branch)
            self.UnSAT += 1
            self.restore_state()
# we need to fix this I don't know where to put the save and return to states ahh
    def handle_while_statement(self, node):
    # Handles while loops by repeatedly checking loop condition feasibility
    # and traversing the loop body as long as the condition holds
        condition_node = node.child_by_field_name('condition').children[1]
        body_node = node.child_by_field_name('body')


        while True:
            self.save_state()
            if self.check_feasibility(condition_node):
                print("Loop condition is UNSAT, breaking")
                #self.restore_state()
                break
            else:
                print("Loop condition is SAT, continuing")
                self.traverse_node(body_node)
                #self.restore_state()

            # Update path condition to prevent infinite loops
            #self.current_path_condition = And(self.current_path_condition, Not(condition_node))
        
    def handle_return(self, node):
        # Processes return statements, checking if they meet the target condition
        return_value_node = node.child_by_field_name('value')
        if return_value_node is not None:
            return_value = self.evaluate_expression(return_value_node)
            if return_value == IntVal(1):
                # Increments target counter if the return value matches target
                self.targetReached += 1
                print("Target reached!")
            else:
                print("Non-target return reached")


    def z3_condition_add(self, solver, op, left, right):
        # Applies basic operators in Z3 to form a symbolic expression
        if op == '+':
            solver.add(left + right)
        elif op == '-':
            solver.add(left - right)
        elif op == '*':
            solver.add(left * right)
        elif op == '/':
            solver.add(left / right)
        elif op == '==':
            solver.add(left == right)
        elif op == '<':
            solver.add(left < right)
        elif op == '>':
            solver.add(left > right)
        elif op == '=':
            solver.add(left == right)
        elif op == '++':
            solver.add(left + 1 == right)
        elif op == '--':
            solver.add(left - 1 == right)
        return

    def check_feasibility(self, condition):
        solver = Solver()

        # initializing all the variables
        for identifier in self.mapping:
            unique_id = Int(identifier)

        # add any previous conditions
        for c in self.condition:
            op = self.condition[c].children[1].text.decode()
            right = self.condition[c].children[0].text.decode()
            left = self.condition[c].children[2].text.decode()
            self.z3_condition_add(solver,op, left, right)

        op = condition.children[1].text.decode()
        right = condition.children[0].text.decode()
        left = condition.children[2].text.decode()
        self.z3_condition_add(solver,op, left, right)

        result = solver.check() == sat
        return result


def main():
    # I am lazy and don't want to run from the command line everytime, un comment out later.
    # parser_args = argparse.ArgumentParser(description="Parse a C file using Tree-sitter.")
    # parser_args.add_argument("c_file", help="Path to the C file to parse.")
    # parser_args.add_argument("function",help="Function to symbolically execute")

    # args = parser_args.parse_args()
    ## Read C code from the file
    # c_code = read_c_code_from_file(args.c_file)

    # Get file path to the c file in question.
    current_directory = os.getcwd()
    file_name = "test_program.c"
    file_path = os.path.join(current_directory, file_name)

    # read in c code
    c_code = read_c_code_from_file(file_path)

    # parse the code using tree sitter
    tree = parser.parse(c_code)

    # printing out the tree
    root_node = tree.root_node
    # print_tree(root_node)
    # function_to_execute = args.function
    function_to_execute = 'main'
    executor = SymbolicExecutor()
    executor.execute(root_node, function_to_execute)

    print("done")


main()

# def evaluate_expression(self, node):
#     # Converts various expression types into Z3 symbolic expressions
#     if node.type == 'identifier':
#         # Resolves variable identifier to its symbolic variable
#         var_name = node.text.decode()
#         # if this value has conditions on it already.
#         if var_name in self.mapping:
#             value = self.mapping[var_name]
#
#         else:
#             value = Int(var_name)
#
#         return value
#     elif node.type == 'number_literal':
#         # Handles numeric literals directly
#         return IntVal(int(node.text.decode()))
#     elif node.type == 'binary_expression':
#         # Evaluates binary expressions recursively
#         left = self.evaluate_expression(node.child_by_field_name('left'))
#         right = self.evaluate_expression(node.child_by_field_name('right'))
#         op = node.child_by_field_name('operator').text.decode()
#         return self.apply_operator(op, left, right)
#     return None
#
# def apply_operator(self, op, left, right):
#     # Applies basic operators in Z3 to form a symbolic expression
#     if op == '+':
#         return left + right
#     elif op == '-':
#         return left - right
#     elif op == '*':
#         return left * right
#     elif op == '/':
#         return left / right
#     elif op == '==':
#         return left == right
#     elif op == '<':
#         return left < right
#     elif op == '>':
#         return left > right
#     elif op == '=':
#         return left == right
#     return None
