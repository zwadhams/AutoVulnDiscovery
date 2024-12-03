from flow_function import FlowFunction

# top equals all declarations
#

class VariableReachabilityFlowFunction(FlowFunction):
    def __init__(self, defs):
        """
        Initialize the flow function with the set of definitions in the program.
        :param defs: A dictionary mapping variables to the set of statements that define them.
        """
        self.defs = defs  # Used to calculate the KILL set

    def top_value(self):
        return set()  # Top of the lattice: empty set, no definitions

    def bottom_value(self):
        return set()  # Bottom of the lattice: empty set, no definitions

    def join(self, val1, val2):
        """
        Compute the join of two sets of reaching definitions.
        :param val1: A set of definitions.
        :param val2: A set of definitions.
        :return: The union of the two sets.
        """
        return val1 | val2  # Join is union for reaching definitions

    def flow_function(self, input_state, instruction):
        """
        Compute the new state given the current state and an instruction.
        :param input_state: The current set of reaching definitions (a set of definitions).
        :param instruction: An Instruction object with type and details.
        :return: The updated set of reaching definitions.
        """
        new_state = input_state.copy()  # Start with the current state

        instr_type = instruction.instr_type
        details = instruction.details

        if instr_type == "assign_const":
            # Handle constant assignment: x := c
            var = details["var"]
            gen = {f"{var}{instruction.line_num}"}  # GEN set: current definition
            kill = {f"{var}{line}" for line in self.defs.get(var, set())}  # KILL set: previous definitions of var

            # Ensure the variable has an entry in the state
            if var not in new_state:
                new_state[var] = set()

            # Apply GEN and KILL
            new_state[var] = (new_state[var] - kill) | gen

        elif instr_type == "assign_var" or instr_type == "binary_op":
            # Handle variable assignment: x := y
            var1 = details["var1"]  # Left-hand side of assignment
            var2 = details["var2"]  # Right-hand side of assignment

            gen = {f"{var1}{instruction.line_num}"}  # GEN set: current definition
            kill = {f"{var1}{line}" for line in self.defs.get(var1, set())}  # KILL set: previous definitions of var1

            # Ensure the variable has an entry in the state
            if var1 not in new_state:
                new_state[var1] = set()

            # Apply GEN and KILL
            new_state[var1] = (new_state[var1] - kill) | gen


        # elif instr_type == "binary_op":
        #     # Handle binary operations: z := x + y, z := x * y, etc.
        #     var = details["var"]  # The result variable
        #     gen = {f"{var}{instruction.line_num}"}  # GEN set: new definition for the result
        #     kill = {f"{var}{line}" for line in self.defs.get(var, set())}  # KILL set: previous definitions of var
        #
        #
        #     new_state = (new_state[var] - kill) | gen  # Apply GEN and KILL

        elif instr_type in {"goto", "conditional"}:
            # Control-flow instructions: they do not directly modify GEN or KILL
            pass

        elif instr_type == "halt":
            # Halt: no modifications to reaching definitions
            pass

        return new_state
