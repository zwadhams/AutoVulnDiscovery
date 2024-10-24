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
solver = Solver()


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
        self.solver = Solver()
        self.symbolic_state = {}
        self.path_conditions = []
        self.functions = {}
        self.var_names = []
        self.current_path_condition = BoolVal(True)
        self.SAT = 0 # num of Feasible paths
        self.UnSAT = 0 # num of infeasible paths
        self.targetReached = 0 # num of paths that reached target note (targetReached<SAT)


    def execute(self, root_node,function):
        #first find all the functions and declared variables.
        self.Find_Functions(root_node)

        # Then Start at the correct function and go through the steps.
        node = self.functions[function]
        self.traverse_node(node)

        #print outputs:
        print("Number of infeasible states:" , self.UnSAT)
        print("Number of feasible states:" , self.SAT)
        print("Number of Target reached: ", self.targetReached)
        print("states: ", self.path_conditions)

    def Find_Functions(self,node):
    ## First we need to find the functions, so we can start at the one we want
    ## we also add in the variables that get declared, so that we can account for global ones later

        if node.type == 'function_definition':
            declarator_node = node.child_by_field_name('declarator')
            function_name_node = declarator_node.children[0]  # Get the function name
            function_name = function_name_node.text.decode('utf-8')  # Decode it to a string
            self.functions[function_name] = node  # Store the function name and corresponding node
            print("Function found: ",function_name)

        # keep track of names declared, adding them to the symbolic state here to handle global values
        elif node.type == 'declaration':
            self.handle_declaration(node)

        else:
            # not a function so we pass
            pass

        # Recursively visit children nodes
        for child in node.children:
            self.Find_Functions(child)

    def traverse_node(self,node):

        if node is None:
            return

        elif node.type =='call_expression':
            function_name =node.children[0]
            print(function_name.text.decode('utf-8'))
            if function_name.text.decode('utf-8') in self.functions:
                self.traverse_node(self.functions[function_name.text.decode('utf-8')])
        elif node.type == 'declaration':
            self.handle_declaration(node)
        elif node.type == 'assignment_expression':
            self.handle_assignment(node)
        elif node.type == 'if_statement':
            self.handle_if_statement(node)
        elif node.type == 'while_statement':
            self.handle_while_statement(node)
        elif node.type == 'return_statement':
            self.handle_return(node)
        else:
            print("not handled",node)

        
        # Recursively visit children nodes
        for child in node.children:
            self.traverse_node(child)
        return

    def handle_function_definition(self, node):
        print(node.children)
        for child in node.children:
            self.traverse_node(child)

    def handle_declaration(self, node):
        # Extract variable name and initial value (if any)
        var_name = node.child_by_field_name('declarator').text.decode()
        init_value = node.child_by_field_name('value')
        if init_value is not None:
            # Handle initialization with a symbolic value
            sym_value = self.evaluate_expression(init_value)
            self.symbolic_state[var_name] = sym_value
        else:
            # If no initial value, create an unconstrained symbolic variable
            self.symbolic_state[var_name] = Int(var_name)
        print(f"Declared variable {var_name} with value {self.symbolic_state[var_name]}")

    def handle_assignment(self, node):
        var_name = node.child_by_field_name('left').text.decode()
        expr = node.child_by_field_name('right')
        value = self.evaluate_expression(expr)
        self.symbolic_state[var_name] = value
        print(f"Assigned {var_name} = {value}")

    def handle_if_statement(self, node):

        condition_p = node.children[1]
        # Process the condition and branches
        condition_node = condition_p.children[1]
        true_branch = node.child_by_field_name('consequence')
        false_branch = node.child_by_field_name('alternative')

        condition = self.evaluate_expression(condition_node)
        true_condition = And(self.current_path_condition, condition)
        false_condition = And(self.current_path_condition, Not(condition))

        # Branch on the true condition
        self.solver.push()
        self.solver.add(true_condition)
        if self.solver.check() == sat:
            self.current_path_condition = true_condition
            self.traverse_node(true_branch)
            self.SAT = self.SAT +1
        self.solver.pop()

        # Branch on the false condition
        self.solver.push()
        self.solver.add(false_condition)
        if self.solver.check() == unsat:
            self.current_path_condition = false_condition
            self.traverse_node(false_branch)
            self.UnSAT = self.UnSAT +1
        self.solver.pop()

    def handle_while_statement(self, node):
        # Loop until the condition becomes unsat
        condition_node = node.child_by_field_name('condition')
        body_node = node.child_by_field_name('body')

        while True:
            condition = self.evaluate_expression(condition_node.children[1])
            loop_condition = And(self.current_path_condition, condition)

            self.solver.push()
            self.solver.add(loop_condition)
            if self.solver.check() == sat:
                print("Loop condition is SAT, continuing")
                self.SAT += 1
                self.current_path_condition = loop_condition
                self.traverse_node(body_node)
            else:
                print("Loop condition is UNSAT, breaking")
                self.UnSAT += 1
                break
            self.solver.pop()

            # Add negation of condition to block further execution
            self.current_path_condition = And(self.current_path_condition, Not(condition))

    def handle_return(self, node):
        # Track the return value and add it to the constraints
        return_value_node = node.children[1]
        if return_value_node is not None:
            return_value = self.evaluate_expression(return_value_node)
            print(f"Return value: {return_value}")
            self.solver.add(self.current_path_condition == return_value)
            if return_value_node.text.decode('utf-8') == 1:
                self.targetReached = self.targetReached +1
                self.path_conditions.append(self.current_path_condition)

    def evaluate_expression(self, node):
        # Evaluate expressions such as binary operations, literals, etc.
        if node.type == 'identifier':
            var_name = node.text.decode()
            return self.symbolic_state.get(var_name, Int(var_name))
        elif node.type == 'number_literal':
            return IntVal(int(node.text.decode()))
        elif node.type == 'binary_expression':
            left = self.evaluate_expression(node.child_by_field_name('left'))
            right = self.evaluate_expression(node.child_by_field_name('right'))
            op = node.child_by_field_name('operator').text.decode()
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '==':
                return left == right
            elif op == '<':
                return left < right
            elif op == '>':
                return left > right
        # Add support for other types of expressions as needed
        return None

def main():

    # I am lazy and don't want to run from the command line everytime, un comment out later.
    #parser_args = argparse.ArgumentParser(description="Parse a C file using Tree-sitter.")
    #parser_args.add_argument("c_file", help="Path to the C file to parse.")
    #parser_args.add_argument("function",help="Function to symbolicly execute")

    #args = parser_args.parse_args()
    ## Read C code from the file
    #c_code = read_c_code_from_file(args.c_file)

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
    #print_tree(root_node)
    #function_to_execute = args.function
    function_to_execute = 'main'
    executor = SymbolicExecutor()
    executor.execute(root_node,function_to_execute)

    print("done")




main()



