import argparse
from z3 import *
import tree_sitter_c as tsc
from tree_sitter import Language, Parser
import os




# conditions shouldn't be attached to specific symbolic vars, just left and right sides if left side is an operations do some step.
# need to updated conditions to handle the left side. so X = X+Y doesn't feed the solver X0 = X+Y  should be X0 = X0 + X1 for example.

C_LANG = Language(tsc.language())
parser = Parser(C_LANG)



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

        # Dictionary to store function nodes, allowing for function calls
        self.functions = {}
        # Maps variable names to their SymbolicVariable instances
        self.mapping = {}
        # Counter for generating unique variable identifiers
        self.counter = 0
        self.condition = []
        self.current_path_condition = BoolVal(True)
        # Stack to save and restore states for branching
        self.saved_states = []
        # Counters to track feasible and infeasible paths
        self.SAT = 0
        self.UnSAT = 0
        # Counter for paths that meet the target condition `return 1;`
        self.targetReached = 0

    def save_state(self,next_node):
        # Saves the current state by storing the path condition,
        # variable mappings, and counter in the saved states stack.
        state = {
            "conditions": self.condition,
            "mapping": self.mapping.copy(),
            "counter": self.counter,
            "next_state": next_node
            # add next state to execute
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
            return state["next_state"]

        else:
            print("No saved state to restore.")
        return

    def execute(self, root_node, function):
        # Main entry point to execute the symbolic interpreter on a function
        # Parses all functions from the root node and then begins traversing
        # the specified function node
        self.find_functions(root_node)
        node = self.functions[function]
        self.traverse_node(node)
        # Outputs results on paths after execution
        print("Number of infeasible states:", self.UnSAT)
        print("Number of feasible states:", self.SAT)
        print("Number of Target reached:", self.targetReached)

    def find_functions(self, node):
        # Recursive function to locate and store all function definitions
        # within the code tree. Assumes function name is the first child node.
        if node.type == 'function_definition':
            declarator_node = node.child_by_field_name('declarator')
            function_name_node = declarator_node.children[0]
            function_name = function_name_node.text.decode('utf-8')
            self.functions[function_name] = node
            print("Function found:", function_name)
        for child in node.children:
            self.find_functions(child)

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
                self.condition.append([self.mapping[var_name][-1], '++', '1', False])
            elif expression_text.endswith('--'):
                var_name = expression_text[:-2].strip()
                self.condition.append([self.mapping[var_name][-1], '--', '1', False])
        elif (node.type == 'declaration') or (node.type =='parameter_declaration'):
            # Declaration node for new variable declarations
            self.handle_declaration(node)
        elif node.type == 'assignment_expression':
            # Assignment node for updating variable values
            self.handle_assignment(node)
        elif node.type == 'if_statement':
            # Conditional branching also we traverse nodes in here, so the next node should be the end of the if statement here
            self.handle_if_statement(node)
            node = node.next_sibling # want to skip ahead, the inside of this "traverse" has been handled in the if function

        elif node.type == 'while_statement':
            self.handle_while_statement(node)
            node = node.next_sibling  # want to skip ahead, the inside of this "traverse" has been handled in the while function

        elif node.type == 'return_statement':
            self.handle_return(node)
        else:
            pass

        # Recursively traverses child nodes
        for child in node.children:
            self.traverse_node(child)

    def z3_condition_add(self, solver, op, left, right,inv):
        # Applies basic operators in Z3 to form a symbolic expression
        # fix
        if op == '+':
            solver.add(left + right)
        elif op == '-':
            solver.add(left - right)
        elif op == '*':
            solver.add(left * right)
        elif op == '/':
            solver.add(left / right)
        elif op == '==':
            if inv:
                solver.add(not(left == right))
            else:
                solver.add(left == right)
        elif op == '<':
            if inv:
                solver.add(not(left<right))
            else:
                solver.add(left < right)
        elif op == '>':
            if inv:
                solver.add(not(left>right))
            else:
                solver.add(left > right)
        elif op == '=':
            solver.add(left == right)
        elif op == '++':
            solver.add(Int(left) == Int(left) + 1)
        elif op == '--':
            solver.add(Int(left) == Int(left) - 1)
        return

    def check_feasibility(self, condition,inv):
        solver = Solver()


        for identifier, assignments in self.mapping.items():
            if assignments:  # Check if there are any assignments in the list
                # Get the most recent assignment (last item in the list)
                most_recent_assignment = assignments[-1]
                unique_id = Int(most_recent_assignment)
                solver.add(Distinct(unique_id)) # add variables to the solver.


        # add any previous conditions
        for c in self.condition:
                op = c[1]
                right = c[0]
                left = c[2]
                inv = c[3]
                self.z3_condition_add(solver, op, left, right,inv)

        op = condition.children[1].text.decode()
        right = condition.children[0].text.decode()
        left = self.mapping[condition.children[2].text.decode()][-1]
        self.z3_condition_add(solver,op, left, right,inv)

        result = solver.check() == sat
        return result

    def handle_declaration(self, node):
        # Just getting the values
        dNode = node.child_by_field_name('declarator')

        # Generates a unique identifier for the symbolic variable
        symbolic_var = f'X{self.counter}'
        self.counter += 1  # add to counter so ids are unique.

        if not dNode.children:
            # create a mapping for example int x: x->X1
            # Initialize the stack for this variable if it doesn't exist
            self.mapping[dNode.text.decode()] = []
            # Append the new assignment to the list (stack behavior)
            self.mapping[dNode.text.decode()].append(symbolic_var)
            print(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")
        else:
            # x1-> c[[X1,<,10,False],[X1 = 10]]

            var_name = dNode.children[0].text.decode()
            # Initialize the stack for this variable if it doesn't exist
            self.mapping[var_name] = []
            # Append the new assignment to the list (stack behavior)
            self.mapping[var_name].append(symbolic_var)

            left = dNode.children[2]
            if left.type == 'call_expression':
                # this is a function, and we just want this symbolic var to be a generic Int to the solver
                # later when we feed the mappings to the solver this will happen (Int(symbolic_var))
                print(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")
                pass

            else:
                # conditions, operator, right and left side of the variable
                op = dNode.children[1].text.decode()
                right = dNode.children[0].text.decode() # we decide later how to handle this side
                inv = False  # for not conditions only with boolean operators.

                self.condition.append([op, right, self.mapping[left.text.decode()][-1], inv])
                print(f" {dNode.text.decode()} mapped to {symbolic_var}")

    def handle_assignment(self, node):

        # Updates a variable with a new condition
        var_name = node.child_by_field_name('left').text.decode()
        if var_name in self.mapping:
            symbolic_var = self.mapping[var_name][-1] # most recent symbolic var added to the stack for this variable.

            # conditions, operator, right and left side of the variable
            op = node.children[1].text.decode()
            right = node.children[0].text.decode()
            left = node.children[2].text.decode()
            inv = False  # for not conditions only with boolean operators.
            self.condition.append([op, right, self.mapping[left][-1], inv])
            print(f"Assigned {var_name} = {node} ")
        else:
            print(f"{var_name} assinging value that hasn't been defined")

    def handle_if_statement(self, node):
        # Handles if statements by creating branches for true and false conditions
        condition_node = node.child_by_field_name('condition')
        true_branch = node.child_by_field_name('consequence')
        false_branch = node.child_by_field_name('alternative')

        new_condition = condition_node.children[1]

        # True branch feasibility check and traversal if feasible
        if self.check_feasibility(new_condition,False):
            # add the new condition to the branches
            op = new_condition.children[1].text.decode()
            right = self.mapping[new_condition.children[0].text.decode()][-1]
            left = self.mapping[new_condition.children[2].text.decode()][-1]
            self.condition.append([right,op,left,False])

            print("if statement", new_condition.text.decode())
            self.SAT += 1  # satisfiable condition
            self.save_state(node.next_sibling)  # save the state and then traverse this branch
            self.traverse_node(true_branch)
        else:
            self.UnSAT += 1

        # False branch feasibility check and traversal if feasible
        if (self.check_feasibility(new_condition,True)) and (false_branch is not None):
            print("Else statement", new_condition.text.decode())
            # add the new condition to the branches
            op = new_condition.children[1].text.decode()
            right = self.mapping[new_condition.children[0].text.decode()][-1] # get symbolic var at this point
            left = self.mapping[new_condition.children[2].text.decode()][-1]  # get symbolic var at this point
            self.condition.append([right, op, left, True])

            self.save_state(node.next_sibling)
            self.traverse_node(false_branch)
            self.SAT += 1

        else:
            self.UnSAT += 1
        return

    def handle_while_statement(self, node):
        # Handles while loops by repeatedly checking loop condition feasibility
        # and traversing the loop body as long as the condition holds
        condition_node = node.child_by_field_name('condition').children[1]
        body_node = node.child_by_field_name('body')
        self.save_state(node.next_sibling)
        while True:

            if self.check_feasibility(condition_node,False):

                print("Loop condition is SAT, continuing")
                self.traverse_node(body_node)  # while it's feasible traverse the node when the nodes done we should go back
                self.SAT = self.SAT +1
            else:
                print("Loop condition is UNSAT, breaking")
                self.UnSAT = self.UnSAT + 1
                self.restore_state()  # if it wasn't feasible, we want to pop the state we just added
                break


        return

    def handle_return(self, node):
        # Processes return statements, checking if they meet the target condition
        return_value_node = node.child_by_field_name('value')
        if return_value_node is not None:
            return_value = return_value_node
            if return_value == IntVal(1):
                # Increments target counter if the return value matches target
                self.targetReached += 1
                print("Target reached!")

            else:
                print("Non-target return reached")
        self.restore_state()
        return # go back to the last branch


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
    function_to_execute = 'test'
    executor = SymbolicExecutor()
    executor.execute(root_node, function_to_execute)

    print("done")


main()

