from abc import ABC, abstractmethod

class FlowFunction(ABC):
    @abstractmethod
    def apply(self, node, input_state):
        """
        Compute the output state for the given node and input state.
        """
        pass
