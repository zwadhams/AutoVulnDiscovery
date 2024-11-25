from flow_function import FlowFunction

'''class IntegerSignAnalysisFlowFunction(FlowFunction):
    def alpha(self, value):
        """Map concrete integers to abstract values."""
        if value == 0:
            return "Z"
        elif value > 0:
            return "P"
        elif value < 0:
            return "N"
        else:
            return "T"  # For unknown or undefined values

    def flow_function(self, input_state, instruction):
        """
        Compute the new state given the current state and an instruction.

        :param state: Current variable state (dict: var -> abstract value).
        :param instruction: An Instruction object.
        :return: New state after applying the instruction.
        """
        new_state = input_state.copy()  # Start with a copy of the current state

        if instruction.instr_type == "assign_const":
            # Assign a constant to a variable
            var = instruction.details["var"]
            const = instruction.details["const"]
            new_state[var] = self.alpha(const)

        elif instruction.instr_type == "assign_var":
            # Assign the value of one variable to another
            var1 = instruction.details["var1"]
            var2 = instruction.details["var2"]
            new_state.setdefault(var1, "⊥")
            new_state[var1] = input_state.get(var2, "⊥")

        elif instruction.instr_type == "binary_op":
            # Perform a binary operation
            var = instruction.details["var"]
            var1 = instruction.details["var1"]
            op = instruction.details["op"]
            var2 = instruction.details["var2"]

            # Get the abstract values of the operands
            val1 = input_state.get(var1, "⊥")
            val2 = input_state.get(var2, "⊥")

            # Abstract operation handling
            if op == "+":
                new_state[var] = self.add_signs(val1, val2)
            elif op == "-":
                new_state[var] = self.subtract_signs(val1, val2)
            elif op == "*":
                new_state[var] = self.multiply_signs(val1, val2)
            elif op == "/":
                new_state[var] = self.divide_signs(val1, val2)

        elif instruction.instr_type in {"goto", "conditional"}:
            # Control flow instructions do not directly affect state
            pass

        elif instruction.instr_type == "halt":
            # No effect on the state
            pass

        return new_state

    def add_signs(self, val1, val2):
        """Abstract addition."""
        print(f"Adding signs: {val1} + {val2}")
        if "T" in {val1, val2}:
            return "T"
        if val1 == "Z":
            return val2
        if val2 == "Z":
            return val1
        if val1 == val2:  # P + P = P, N + N = N
            return val1
        return "T"  # P + N = T (unknown)

    def subtract_signs(self, val1, val2):
        """Abstract subtraction."""
        if "T" in {val1, val2}:
            return "T"
        if val1 == "Z":
            return val2 if val2 == "Z" else "T"
        if val2 == "Z":
            return val1
        if val1 == val2:  # P - P = Z, N - N = Z
            return "Z"
        return "T"  # P - N = T (unknown)

    def multiply_signs(self, val1, val2):
        """Abstract multiplication."""
        if "T" in {val1, val2}:
            return "T"
        if val1 == "Z" or val2 == "Z":
            return "Z"
        if val1 == val2:  # P * P = P, N * N = P
            return "P"
        return "N"  # P * N = N

    def divide_signs(self, val1, val2):
        """Abstract division."""
        if "T" in {val1, val2} or val2 == "Z":
            return "T"  # Division by zero or unknown
        if val1 == "Z":
            return "Z"
        if val1 == val2:  # P / P = P, N / N = P
            return "P"
        return "N"  # P / N = N
'''

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


