class DefinitionExtractor:
    def __init__(self, instructions):
        """
        Initializes the extractor with a list of parsed instructions.
        :param instructions: List of parsed instructions.
        """
        self.instructions = instructions
        self.definitions = self.extract_definitions()

    def extract_definitions(self):
        """
        Extracts all variable definitions from the list of parsed instructions.
        :return: A dictionary mapping variables to the set of line numbers where they are defined.
        """
        defs = {}

        for instr in self.instructions:
            line_num = instr.line_num
            instr_type = instr.instr_type
            details = instr.details

            if instr_type in {"assign_const", "assign_var", "binary_op"}:
                var = details.get("var") or details.get("var1")
                if var:
                    if var not in defs:
                        defs[var] = set()
                    defs[var].add(line_num)

        return defs

    def print_definitions(self):
        """Prints the extracted definitions in a readable format."""
        for var, lines in self.definitions.items():
            lines_str = ", ".join(map(str, sorted(lines)))
            print(f"{var}: {lines_str}")