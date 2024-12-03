import re
from instruction import Instruction

class Parser:
    def __init__(self, file_path):
        # Initialize the parser with a file path and prepare to parse instructions
        self.file_path = file_path
        self.instructions = []

        # Regular expressions to match different instruction patterns in the file
        self.line_number_re = re.compile(r"^(\d+):\s*(.*)$")  # Matches lines starting with a number followed by a colon
        self.assign_const_re = re.compile(r"(\w+)\s*:=\s*(-?\d+)")  # Matches assignment of a constant value to a variable
        self.assign_var_re = re.compile(r"(\w+)\s*:=\s*(\w+)")  # Matches assignment of a variable to another variable
        self.binary_op_re = re.compile(r"(\w+)\s*:=\s*(\w+)\s*([+\-*/])\s*(\w+)")  # Matches binary operations (e.g., addition)
        self.goto_re = re.compile(r"goto\s+(\d+)")  # Matches unconditional goto statements
        self.conditional_goto_re = re.compile(r"if\s+(\w+)\s*([<>=!]+)\s*0\s*:?\s*goto\s+(\d+)")  # Matches conditional goto statements
        self.halt_re = re.compile(r"halt")  # Matches the halt instruction

        # Parse the given file to extract instructions
        self.parse_w3a()

    def parse_w3a(self):
        """
        Parses a file containing instructions formatted in a custom assembly-like language.
        Each line is expected to have a line number followed by an instruction.
        """
        with open(self.file_path, 'r') as file:
            for line in file:
                # Strip whitespace and skip empty lines
                line = line.strip()
                if not line:
                    continue

                # Extract the line number and instruction part
                match = self.line_number_re.match(line)
                if not match:
                    raise SyntaxError(f"Invalid format for line: {line}")
                line_num, instruction = match.groups()
                line_num = int(line_num)

                # Check if the instruction is a halt operation
                if self.halt_re.match(instruction):
                    self.instructions.append(Instruction(line_num, "halt"))
                    continue

                # Check if the instruction is an assignment of a constant value to a variable
                match = self.assign_const_re.match(instruction)
                if match:
                    var, const = match.groups()
                    self.instructions.append(Instruction(line_num, "assign_const", var=var, const=int(const)))
                    continue

                # Check if the instruction is an assignment of one variable to another
                match = self.assign_var_re.match(instruction)
                if match:
                    var1, var2 = match.groups()
                    self.instructions.append(Instruction(line_num, "assign_var", var1=var1, var2=var2))
                    continue

                # Check if the instruction is a binary operation (e.g., addition, subtraction, multiplication, division)
                match = self.binary_op_re.match(instruction)
                if match:
                    var, var1, op, var2 = match.groups()
                    self.instructions.append(Instruction(line_num, "binary_op", var=var, var1=var1, op=op, var2=var2))
                    continue

                # Check if the instruction is a conditional jump (goto) based on a comparison involving a variable
                match = self.conditional_goto_re.match(instruction)
                if match:
                    var, op, target = match.groups()
                    self.instructions.append(Instruction(line_num, "conditional", var=var, op=op, target=int(target)))
                    continue

                # Check if the instruction is an unconditional jump (goto)
                match = self.goto_re.match(instruction)
                if match:
                    target = match.group(1)
                    self.instructions.append(Instruction(line_num, "goto", target=int(target)))
                    continue

    def get_instructions(self):
        """
        Returns the list of parsed instructions.
        """
        return self.instructions
