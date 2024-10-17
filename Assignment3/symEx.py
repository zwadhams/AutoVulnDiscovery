import argparse
from z3 import *
import tree_sitter_c as tsc
from tree_sitter import Language, Parser

C_LANG = Language(tsc.language())
parser = Parser(C_LANG)

# Example path: Assignment3\test_program.c
def read_c_code_from_file(file_path):
    with open(file_path, 'rb') as file:  # Read as bytes
        return file.read()
    
def print_tree(node, indent=""):
    print(f"{indent}{node.type} [{node.start_point}, {node.end_point}]")
    for child in node.children:
        print_tree(child, indent + "  ")

def main():
    # Parse command line arguments
    parser_args = argparse.ArgumentParser(description="Parse a C file using Tree-sitter.")
    parser_args.add_argument("c_file", help="Path to the C file to parse.")
    args = parser_args.parse_args()

    # Read C code from the file
    c_code = read_c_code_from_file(args.c_file)

    # Parse the C code
    tree = parser.parse(c_code)

    # Get the root node of the syntax tree
    root_node = tree.root_node

    # Print the syntax tree
    print_tree(root_node)

main()