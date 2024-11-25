class CFG:
    def __init__(self, instructions):
        self.cfg = self.create_cfg(instructions)
    
    def create_cfg(self, instructions):
        cfg = {}  # Initialize the control flow graph

        # Map line numbers to instructions for quick lookup
        instr_map = {instr.line_num: instr for instr in instructions}

        for instr in instructions:
            line_num = instr.line_num
            instr_type = instr.instr_type
            details = instr.details

            # Initialize the successors for this instruction
            cfg[line_num] = []

            # Sequential instructions (assign_const, assign_var)
            if instr_type in {"assign_const", "assign_var"}:
                next_line = line_num + 1
                if next_line in instr_map:
                    cfg[line_num].append(next_line)

            # Halt instruction
            elif instr_type == "halt":
                # Halt has no successors
                cfg[line_num] = []

            # Debug: Print the current instruction and its successors
            #print(f"Instruction Line {line_num}: {instr_type}, Successors: {cfg[line_num]}")

        return cfg
