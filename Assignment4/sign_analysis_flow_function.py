from flow_function import FlowFunction

class IntegerSignAnalysisFlowFunction(FlowFunction):
    def top_value(self):
        return "T"  # Top of the lattice

    def bottom_value(self):
        return "⊥"  # Bottom of the lattice

    def join(self, val1, val2):
        if val1 == val2:
            return val1
        if "T" in {val1, val2}:
            return "T"
        if val1 == "⊥":
            return val2
        if val2 == "⊥":
            return val1
        return "T"

    def flow_function(self, input_state, instruction):
        new_state = input_state.copy()
        if instruction.instr_type == "assign_const":
            var = instruction.details["var"]
            const = instruction.details["const"]
            if const == 0:
                new_state[var] = "Z"
            elif const > 0:
                new_state[var] = "P"
            elif const < 0:
                new_state[var] = "N"
        elif instruction.instr_type == "assign_var":
            var1 = instruction.details["var1"]
            var2 = instruction.details["var2"]
            new_state[var1] = input_state.get(var2, self.bottom_value())
        elif instruction.instr_type == "binary_op":
            # Handle abstract operations like addition or subtraction
            pass  # Use the logic from the improved algorithm
        return new_state


