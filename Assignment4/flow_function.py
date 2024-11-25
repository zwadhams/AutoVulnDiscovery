from abc import ABC, abstractmethod

'''class FlowFunction(ABC):
    @abstractmethod
    def alpha(self, value):
        """
        Map concrete values to abstract values.
        """
        pass
    
    @abstractmethod
    def flow_function(self, input_state, instruction):
        """
        Compute the output state for the given node and input state.
        """
        pass'''

from abc import ABC, abstractmethod

class FlowFunction(ABC):
    @abstractmethod
    def top_value(self):
        """Return the top value of the lattice."""
        pass

    @abstractmethod
    def bottom_value(self):
        """Return the bottom value of the lattice."""
        pass

    @abstractmethod
    def join(self, val1, val2):
        """Join two values in the lattice."""
        pass

    @abstractmethod
    def flow_function(self, input_state, instruction):
        """Apply the flow function to compute the new state."""
        pass