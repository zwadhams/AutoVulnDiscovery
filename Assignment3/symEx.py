import argparse
from z3 import *
import tree_sitter_c as tsc
from tree_sitter import Language, Parser
import os


C_LANG = Language(tsc.language())
parser = Parser(C_LANG)
solver = Solver()


# Example path: Assignment3\test_program.c
def read_c_code_from_file(file_path):
    with open(file_path, 'rb') as file: 
        return file.read()
    
def print_tree(node, indent=""):
    hold = f"{indent}{node.type} "  #  [{node.start_point}, {node.end_point}]
    print(hold)
    for child in node.children:
        print_tree(child, indent + "  ")
    return

# Potential class structure for handling statements
state = {}
# Path constraints (to handle different branches)
path_constraints = []

functions = {}


class VariableDeclaration:
    def __init__(self, var_name):
        self.var_name = var_name

    def execute(self):
        # Declare a symbolic variable in Z3
        state[self.var_name] = Int(self.var_name)
        print(f"Declared variable {self.var_name}")


def execute_statement(statement_node):

    if statement_node.type == 'declaration':
        var_name = statement_node.children[1].text.decode()
        VariableDeclaration(var_name).execute()

    else:
        print("not handled statement: ",statement_node.type)

    # first we execute the statement, then go through all the children nodes
    for child in statement_node.children:
        execute_statement(child)

    # once we are out of children nodes we finish.
    return

def main():

    # I am lazy and don't want to run from the command line everytime, un comment out later.
    #parser_args = argparse.ArgumentParser(description="Parse a C file using Tree-sitter.")
    #parser_args.add_argument("c_file", help="Path to the C file to parse.")
    #args = parser_args.parse_args()
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

    # Get the root node of the syntax tree
    root_node = tree.root_node

    # Print the syntax tree
    print_tree(root_node)

    execute_statement(root_node)

main()