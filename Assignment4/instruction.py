class Instruction:
    def __init__(self, line_num, instr_type, **kwargs):
        self.line_num = line_num
        self.instr_type = instr_type
        self.details = kwargs

    def __repr__(self):
        return f"Line {self.line_num}: {self.instr_type} {self.details}"