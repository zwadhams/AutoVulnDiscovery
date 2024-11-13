import argparse
import logging
import os
import re

class Instruction:
    def __init__(self, line_num, instr_type, **kwargs):
        self.line_num = line_num
        self.instr_type = instr_type
        self.details = kwargs

    def __repr__(self):
        return f"Line {self.line_num}: {self.instr_type} {self.details}"

def parse_w3a(file_path):
    instructions = []
    # Regular expressions for parsing each type of instruction
    assign_const_re = re.compile(r"(\w+)\s*:=\s*(\d+)")
    assign_var_re = re.compile(r"(\w+)\s*:=\s*(\w+)")
    binary_op_re = re.compile(r"(\w+)\s*:=\s*(\w+)\s*([+\-*/])\s*(\w+)")
    goto_re = re.compile(r"goto\s+(\d+)")
    conditional_goto_re = re.compile(r"if\s+(\w+)\s*([<>=!]+)\s*0\s*:\s*goto\s+(\d+)")
    halt_re = re.compile(r"halt")

    # Open the file and parse line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue

            # Check for halt
            if halt_re.match(line):
                instructions.append(Instruction(line_num, "halt"))
                continue

            # Check for assignment of constant
            match = assign_const_re.match(line)
            if match:
                var, const = match.groups()
                instructions.append(Instruction(line_num, "assign_const", var=var, const=int(const)))
                continue

            # Check for assignment of variable
            match = assign_var_re.match(line)
            if match:
                var1, var2 = match.groups()
                instructions.append(Instruction(line_num, "assign_var", var1=var1, var2=var2))
                continue

            # Check for binary operation
            match = binary_op_re.match(line)
            if match:
                var, var1, op, var2 = match.groups()
                instructions.append(Instruction(line_num, "binary_op", var=var, var1=var1, op=op, var2=var2))
                continue

            # Check for unconditional goto
            match = goto_re.match(line)
            if match:
                target = int(match.group(1))
                instructions.append(Instruction(line_num, "goto", target=target))
                continue

            # Check for conditional goto
            match = conditional_goto_re.match(line)
            if match:
                var, cond, target = match.groups()
                instructions.append(Instruction(line_num, "conditional_goto", var=var, cond=cond, target=int(target)))
                continue

            # If we reach here, the line didn't match any known pattern
            raise SyntaxError(f"Unrecognized instruction on line {line_num}: {line}")

    return instructions


def main():
    parser_args = argparse.ArgumentParser(description="Give a W3A file and either signed or reaching for analysis type (ex: python W3A_DataFlow.py prog_1.w3a reaching)")
    parser_args.add_argument("W3A_file", help="Path to the W3A file to analyze.")
    parser_args.add_argument("function", help="Type of flow function, either signed or reaching")
    args = parser_args.parse_args()
    
    # Parse the file and print the instructions
    parsed_instructions = parse_w3a(args.W3A_file)
    for instr in parsed_instructions:
        print(instr)

    return

main()