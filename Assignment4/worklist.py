class Worklist:
    def __init__(self, instructions, flow_function):
        """
        :param instructions: List of parsed instructions.
        :param flow_function: Flow function implementing a specific analysis.
        """
        self.instructions = instructions
        self.flow_function = flow_function
        self.worklist = list(range(1, len(instructions) + 1))  # Initialize worklist
        self.input_states = {n: {} for n in range(1, len(instructions) + 1)}  # Input state for each node
        self.output_states = {n: {} for n in range(1, len(instructions) + 1)}  # Output state for each node
        
        # Initialize input state for the entry node (first instruction)
        for instr in instructions:
            for var in {instr.details.get("var"), instr.details.get("var1"), instr.details.get("var2")}:
                if var:
                    self.input_states[1][var] = self.flow_function.top_value()
        self.print_initial_state()

    def join_states(self, state1, state2):
        """Join two states based on the lattice."""
        new_state = state1.copy()
        for var, val in state2.items():
            new_state[var] = self.flow_function.join(new_state.get(var, self.flow_function.bottom_value()), val)
        return new_state

    def analyze(self):
        """Run the worklist algorithm."""
        iteration = 1
        while self.worklist:
            n = self.worklist.pop(0)
            instruction = self.instructions[n - 1]
            old_output = self.output_states[n].copy()

            # Apply the flow function to compute the output state
            new_output = self.flow_function.flow_function(self.input_states[n], instruction)
            self.output_states[n] = new_output

            # Propagate to successors in the control flow graph
            for successor in self.get_successors(n, instruction):
                new_input = self.join_states(self.input_states[successor], self.output_states[n])
                if new_input != self.input_states[successor]:
                    self.input_states[successor] = new_input
                    if successor not in self.worklist:
                        self.worklist.append(successor)

            # Debug output for iteration
            self.debug_iteration(iteration, n)
            iteration += 1

        return self.input_states, self.output_states

    def get_successors(self, n, instruction):
        """Determine the successors of the current instruction."""
        if instruction.instr_type == "goto":
            return [instruction.details["target"]]
        elif instruction.instr_type == "conditional":
            return [instruction.details["target"], n + 1]
        elif instruction.instr_type == "halt":
            return []
        else:
            return [n + 1] if n + 1 <= len(self.instructions) else []
    
    def print_initial_state(self):
        # Print the header only once
        worklist_str = ', '.join(map(str, self.worklist)) if self.worklist else "empty"
        input_str = ', '.join([f"{k}->{v}" for k, v in self.input_states[1].items()])
        print(f"{'instr':<5} | {'worklist':<35} | {'abstract val':<30}")
        print(f"{0:<5} | {worklist_str:<35} | {input_str:<30}")

    def debug_iteration(self, iteration, node):
        """Print the current state of the worklist and analysis for debugging."""
        worklist_str = ', '.join(map(str, self.worklist)) if self.worklist else "empty"
        output_str = ' '.join([f"{k}->{v}" for k, v in self.output_states[node].items()])
        print(f"{iteration:<5} | {worklist_str:<35} | {output_str:<30}")