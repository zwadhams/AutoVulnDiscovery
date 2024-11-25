from sign_analysis_flow_function import IntegerSignAnalysisFlowFunction
from reachability_flow_function import VariableReachabilityFlowFunction
import logging

logging.basicConfig(level=logging.DEBUG)
'''
class Worklist:
    def __init__(self, cfg, analysis_type):
        """
        Initialize the Worklist algorithm.

        :param cfg: The control flow graph (dictionary of node -> successors).
        :param initial_state: The initial state of the program.
        :param analysis_type: Type of analysis ("signed" or "reachability").
        """
        self.cfg = cfg.cfg
        logging.info(f"CFG: {self.cfg}")
        self.input_states = {n: set() for n in self.cfg}  # Input state for each node
        logging.info(f"Input states: {self.input_states}")
        self.output_states = {n: set() for n in self.cfg}  # Output state for each node
        self.worklist = list(self.cfg.keys())  # All nodes initially in the worklist

        # Select the appropriate flow function
        if analysis_type == "signed":
            self.flow_function = IntegerSignAnalysisFlowFunction()
            logging.info("Using Integer Sign Analysis Flow Function")
        elif analysis_type == "reachability":
            self.flow_function = VariableReachabilityFlowFunction()
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

        # Set the initial state for the program's entry point
        #self.input_states[0] = initial_state

    def run(self):
        """
        Run the worklist algorithm.
        """
        while self.worklist:
            node = self.worklist.pop(0) # This is an int.
            logging.info(f"Processing node {node}")
            logging.info(f"Processing node {type(node)}")
            logging.info(f"Input state: {self.input_states[node]}")
            # Compute the output state for the current node
            new_output = self.flow_function.flow_function(self.input_states[node], node)
            print(f"Node {node}: {new_output}")
            self.output_states[node] = new_output

            # Update successors
            for succ in self.cfg[node]:
                new_input = self.input_states[succ].union(new_output)
                if new_input != self.input_states[succ]:
                    self.input_states[succ] = new_input
                    self.worklist.append(succ)
'''
'''
class Worklist:
    def __init__(self, instructions, lattice, cfg, analysis_type):
        self.lattice = lattice
        self.cfg = cfg.cfg
        self.instructions = instructions
        self.analysis_type = analysis_type

        # Select the appropriate flow function
        if analysis_type == "signed":
            self.flow_function = IntegerSignAnalysisFlowFunction()
            logging.info("Using Integer Sign Analysis Flow Function")
        elif analysis_type == "reachability":
            self.flow_function = VariableReachabilityFlowFunction()
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

    def run(self):
        # Initialize the worklist with all nodes in the CFG
        worklist = list(self.cfg.keys())

        # Initialize input and output states for all nodes
        input_states = {n: {} for n in self.cfg}
        output_states = {n: {} for n in self.cfg}

        # Dynamically add variables to the initial state
        variables = set()  # Collect all variables from the instructions
        for instr in self.instructions:
            if instr.instr_type == "assign_const":
                variables.add(instr.details["var"])
            elif instr.instr_type == "assign_var":
                variables.add(instr.details["var1"])
                variables.add(instr.details["var2"])
            elif instr.instr_type == "binary_op":
                variables.add(instr.details["var"])
                variables.add(instr.details["var1"])
                variables.add(instr.details["var2"])

        # Initialize the entry node (node 1) with all variables set to ⊥
        input_states[1] = {var: "⊥" for var in variables}

        # Add all nodes to the worklist
        for n in self.cfg.keys():
            output_states[n] = {var: "⊥" for var in variables}

        # Print initialized states for debugging
        print("Initialized input states:", input_states)
        print("Initialized output states:", output_states)
        print("Initialized worklist:", worklist)

        '''
'''while worklist:
            n = worklist.pop(0)
            instruction = self.instructions[n - 1]
            output_states[n] = self.flow_function.flow_function(input_states[n], instruction)

            for j in self.cfg[n]:
                new_input = self.join_states(input_states[j], output_states[n])
                if new_input != input_states[j]:
                    input_states[j] = new_input
                    if j not in worklist:
                        worklist.append(j)

            print(f"Processed Node {n}")
            print(f"Input states: {input_states}")
            print(f"Output states: {output_states}")
            print(f"Worklist: {worklist}")'''
'''
        while worklist:
            # Take a node n off the worklist
            n = worklist.pop(0)

            # Apply the flow function for the current node
            instruction = self.instructions[n - 1]
            output_states[n] = self.flow_function.flow_function(input_states[n], instruction)

            # Check successors and propagate state
            if instruction.instr_type == "conditional":
                # Handle both true and false branches
                true_successor = instruction.details["target"]  # The target of the conditional
                false_successor = n + 1  # The next instruction in the program

                # Iterate over both branches
                for successor in [true_successor, false_successor]:
                    new_input = self.join_states(input_states[successor], output_states[n])
                    if new_input != input_states[successor]:
                        input_states[successor] = new_input
                        if successor not in worklist:
                            worklist.append(successor)
            elif instruction.instr_type == "goto":
                # Handle goto by propagating to the target
                target = instruction.details["target"]
                new_input = self.join_states(input_states[target], output_states[n])
                if new_input != input_states[target]:
                    input_states[target] = new_input
                    if target not in worklist:
                        worklist.append(target)
            else:
                # Handle normal (non-conditional) successors from the CFG
                for successor in self.cfg[n]:
                    new_input = self.join_states(input_states[successor], output_states[n])
                    if new_input != input_states[successor]:
                        input_states[successor] = new_input
                        if successor not in worklist:
                            worklist.append(successor)

            # Debugging output
            print(f"Processed Node {n}")
            print(f"Input states: {input_states}")
            print(f"Output states: {output_states}")
            print(f"Worklist: {worklist}")




    def join_states(self, state1, state2):
        # Get all variables present in either state
        all_vars = set(state1.keys()).union(set(state2.keys()))
            
        # Create a new state by joining values for each variable
        new_state = {}
        for var in all_vars:
            value1 = state1.get(var, "⊥")  # Default to bottom if variable is missing
            value2 = state2.get(var, "⊥")  # Default to bottom if variable is missing
            new_state[var] = self.lattice.join(value1, value2)
            
        return new_state

'''



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

    def debug_iteration(self, iteration, node):
        """Print the current state of the worklist and analysis for debugging."""
        worklist_str = ', '.join(map(str, self.worklist)) if self.worklist else "empty"
        input_str = ', '.join([f"{k}->{v}" for k, v in self.input_states[node].items()])
        output_str = ', '.join([f"{k}->{v}" for k, v in self.output_states[node].items()])
        print(f"Iteration {iteration}, Node {node}")
        print(f"  Worklist: {worklist_str}")
        print(f"  Input: {input_str}")
        print(f"  Output: {output_str}")
        print("-" * 50)