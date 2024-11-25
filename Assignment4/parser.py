import re
from instruction import Instruction
class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.instructions = []
        self.line_number_re = re.compile(r"^(\d+):\s*(.*)$")
        self.assign_const_re = re.compile(r"(\w+)\s*:=\s*(-?\d+)")
        self.assign_var_re = re.compile(r"(\w+)\s*:=\s*(\w+)")
        self.binary_op_re = re.compile(r"(\w+)\s*:=\s*(\w+)\s*([+\-*/])\s*(\w+)")
        self.goto_re = re.compile(r"goto\s+(\d+)")
        self.conditional_goto_re = re.compile(r"if\s+(\w+)\s*([<>=!]+)\s*0\s*:?\s*goto\s+(\d+)")
        self.halt_re = re.compile(r"halt")
        self.parse_w3a()
        
    def parse_w3a(self):
        # Open the file and parse line by line
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                # Extract the line number and instruction
                match = self.line_number_re.match(line)
                if not match:
                    raise SyntaxError(f"Invalid format for line: {line}")
                line_num, instruction = match.groups()
                line_num = int(line_num)

                # Check for halt
                if self.halt_re.match(instruction):
                    self.instructions.append(Instruction(line_num, "halt"))
                    continue

                # Check for assignment of constant
                match = self.assign_const_re.match(instruction)
                if match:
                    var, const = match.groups()
                    self.instructions.append(Instruction(line_num, "assign_const", var=var, const=int(const)))
                    continue

                # Check for assignment of variable
                match = self.assign_var_re.match(instruction)
                if match:
                    var1, var2 = match.groups()
                    self.instructions.append(Instruction(line_num, "assign_var", var1=var1, var2=var2))
                    continue

                # Check for binary operation
                match = self.binary_op_re.match(instruction)
                if match:
                    var, var1, op, var2 = match.groups()
                    self.instructions.append(Instruction(line_num, "binary_op", var=var, var1=var1, op=op, var2=var2))
                    continue

                # Check for conditional goto
                match = self.conditional_goto_re.match(instruction)
                if match:
                    var, op, target = match.groups()
                    self.instructions.append(Instruction(line_num, "conditional", var=var, op=op, target=int(target)))
                    continue

                # Check for unconditional goto
                match = self.goto_re.match(instruction)
                if match:
                    target = match.group(1)
                    self.instructions.append(Instruction(line_num, "goto", target=int(target)))
                    continue

    def get_instructions(self):
        return self.instructions