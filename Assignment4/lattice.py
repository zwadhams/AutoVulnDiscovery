class Lattice:
    def __init__(self, analysis):
        if analysis == "signed":
            self.lattice = {
                "⊥": ["Z", "P", "N"],  # Bottom connects to Z, P, N
                "Z": ["T"],            # Z connects to Top
                "P": ["T"],            # P connects to Top
                "N": ["T"],            # N connects to Top
                "T": []                # Top has no outgoing edges
            }
        else:
            self.lattice = {
                "⊥": ["Z", "P", "N"],  # Bottom connects to Z, P, N
                "Z": ["T"],            # Z connects to Top
                "P": ["T"],            # P connects to Top
                "N": ["T"],            # N connects to Top
                "T": []                # Top has no outgoing edges
            }

    # Partial order
    def is_less_than_equal(self, a, b):
        if a == b:
            return True
        visited = set()
        stack = [a]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            if current == b:
                return True
            stack.extend(self.lattice.get(current, []))
        return False

    # Join
    def join(self, a, b):
        if a == b:
            return a
        if a == "⊥":
            return b  # Bottom joins with anything to return the other element
        if b == "⊥":
            return a  # Bottom joins with anything to return the other element
        if a == "T" or b == "T":
            return "T"  # Top joins with anything to return Top

        # Otherwise, find the least common ancestor
        ancestors_a = self.get_ancestors(a)
        ancestors_b = self.get_ancestors(b)
        common = ancestors_a.intersection(ancestors_b)

        # Return the "lowest" (closest to a and b) common ancestor
        for node in self.lattice:  # Traverse lattice order
            if node in common:
                return node

        raise ValueError(f"No join found for {a} and {b}")

    def get_ancestors(self, node):
        """Get all ancestors of a node in the lattice."""
        ancestors = set()
        stack = [node]
        while stack:
            current = stack.pop()
            if current in ancestors:
                continue
            ancestors.add(current)
            stack.extend(self.lattice.get(current, []))  # get is a dictionary method
        return ancestors

    def depth(self, node):
        """Calculate the depth of a node in the lattice."""
        if not self.lattice[node]:
            return 0
        return 1 + max(self.depth(parent) for parent in self.lattice[node])


if __name__ == "__main__":
    l = Lattice("signed")
    print(l.is_less_than_equal("⊥", "T"))  # True
    print(l.is_less_than_equal("T", "⊥"))  # False
    print(l.join("Z", "P"))  # Output: T
    print(l.join("⊥", "P"))  # Output: P
