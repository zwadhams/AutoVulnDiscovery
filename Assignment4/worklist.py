from sign_analysis_flow_function import IntegerSignAnalysisFlowFunction
from reachability_flow_function import VariableReachabilityFlowFunction

class Worklist:
    def __init__(self, cfg, initial_state, analysis_type):
        """
        Initialize the Worklist algorithm.

        :param cfg: The control flow graph (dictionary of node -> successors).
        :param initial_state: The initial state of the program.
        :param analysis_type: Type of analysis ("signed" or "reachability").
        """
        self.cfg = cfg
        self.input_states = {n: set() for n in cfg}  # Input state for each node
        self.output_states = {n: set() for n in cfg}  # Output state for each node
        self.worklist = list(cfg.keys())  # All nodes initially in the worklist

        # Select the appropriate flow function
        if analysis_type == "signed":
            self.flow_function = IntegerSignAnalysisFlowFunction()
        elif analysis_type == "reachability":
            self.flow_function = VariableReachabilityFlowFunction()
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

        # Set the initial state for the program's entry point
        self.input_states[0] = initial_state

    def run(self):
        """
        Run the worklist algorithm.
        """
        while self.worklist:
            node = self.worklist.pop(0)
            # Compute the output state for the current node
            new_output = self.flow_function.apply(node, self.input_states[node])
            self.output_states[node] = new_output

            # Update successors
            for succ in self.cfg[node]:
                new_input = self.input_states[succ].union(new_output)
                if new_input != self.input_states[succ]:
                    self.input_states[succ] = new_input
                    self.worklist.append(succ)
