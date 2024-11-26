class Worklist:
    def __init__(self, instructions, flow_function):
        """
        :param instructions: List of parsed instructions.
        :param flow_function: Flow function implementing a specific analysis.
        """
        self.instructions = instructions
        self.flow_function = flow_function
        self.worklist = list(range(1, len(instructions) + 1))  # Initialize worklist. 
        # Contains the instruction numbers.
        self.input_states = {n: {} for n in range(1, len(instructions) + 1)}  # Holds the state 
        # before each instruction executes. Keys are instruction numbers. Values are initialized 
        # to an empty dictionary. Ex for prog2: input_states: {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
        self.output_states = {n: {} for n in range(1, len(instructions) + 1)}  # Holds the state 
        # after each instruction executes. Keys are instruction numbers. Values are initialized 
        # to an empty dictionary.
        
        
        # Initialize input state for the entry node (first instruction) 
        # Ex for prog2: {1: {'x': 'T'}, 2: {}, 3: {}, 4: {}, 5: {}}
        for instr in instructions:
            for var in {instr.details.get("var"), instr.details.get("var1"), instr.details.get("var2")}:
                if var:
                    self.input_states[1][var] = self.flow_function.top_value()
        self.print_initial_state()

    
    #join_states iterates over the values of the two states and calls the join method of 
    # the flow function to join the values of each variable. If there is a conflict, 
    # the lowest upper bound in the lattice is chosen.
    def join_states(self, state1, state2):
        """Join two states based on the lattice."""
        new_state = state1.copy()
        for var, val in state2.items(): # Iterate over the key-value pairs in state2
            new_state[var] = self.flow_function.join(new_state.get(var, self.flow_function.bottom_value()), val) # Bottom is the default value if the key is not found in new_state. 
        return new_state # Return the new state

    def analyze(self):
        """Run the worklist algorithm."""
        iteration = 1
        while self.worklist:
            current_instruction_number = self.worklist.pop(0)
            parsed_instruction = self.instructions[current_instruction_number - 1] 
            # Instructions object list indexes start at 0. current_instruction_number used 
            # by the worklist start at 1.

            # Apply the flow function to compute the output state.
            # The flow_function takes in a state (ex: {'x': 'T'}) and an Instruction object 
            # and returns an updated analysis state with program variables possibly having 
            # assigned new abstract values new_output (ex: {'x': 'Z'})
            new_output = self.flow_function.flow_function(self.input_states[current_instruction_number], parsed_instruction)
            self.output_states[current_instruction_number] = new_output # Update the output state for the current instruction

            # Update the input state for the successors of the current instruction.
            for successor in self.get_successor_instruction(current_instruction_number, parsed_instruction):
                merged_states = self.join_states(self.input_states[successor], self.output_states[current_instruction_number])
                if merged_states != self.input_states[successor]:
                    self.input_states[successor] = merged_states # Update the input state 
                    # for the successor with the merged state.
                    if successor not in self.worklist: # If we're on a loop, 
                        # we may need to add the successor to the worklist.
                        self.worklist.append(successor)

            # Debug output for iteration
            self.debug_iteration(iteration, current_instruction_number)
            iteration += 1

        return self.input_states, self.output_states

    def get_successor_instruction(self, n, instruction):
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