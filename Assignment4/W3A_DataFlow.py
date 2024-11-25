import argparse
from parser import Parser
from lattice import Lattice
from cfg import CFG
from worklist import Worklist
from sign_analysis_flow_function import IntegerSignAnalysisFlowFunction
from reachability_flow_function import VariableReachabilityFlowFunction
    
def int_sign_analysis(parsed_instructions):
    # Abstract domain values: P (positive), N (negative), Z (zero), T (top/unknown)
    abstract_vals = {}
    worklist = list(range(1, len(parsed_instructions) + 1))  # Initialize worklist to start from instruction 1

    # Initialize all variables to top (T)
    for instr in parsed_instructions:
        if instr.instr_type in ["assign_const", "assign_var", "binary_op"]:
            for var in [instr.details.get("var"), instr.details.get("var1"), instr.details.get("var2")]:
                if var:
                    abstract_vals[var] = "T"

    # Print the initial state before any iteration
    worklist_str = ', '.join(map(str, worklist)) if worklist else "empty"
    abstract_val_str = ', '.join([f"{k}->{v}" for k, v in abstract_vals.items()])
    print(f"instr | worklist | abstract val\n0 | {worklist_str} | {abstract_val_str}")

    # Run the worklist algorithm
    iteration = 1
    while worklist:
        index = worklist.pop(0) - 1  # Adjust index to match 0-based list indexing
        instr = parsed_instructions[index]

        old_vals = abstract_vals.copy()

        if instr.instr_type == "assign_const":
            var = instr.details["var"]
            const = instr.details["const"]
            if const > 0:
                abstract_vals[var] = "P"
            elif const < 0:
                abstract_vals[var] = "N"
            else:
                abstract_vals[var] = "Z"

        elif instr.instr_type == "conditional_goto":
            var = instr.details["var"]
            cond = instr.details["cond"]
            value = instr.details["value"]
            target = instr.details["target"]

            # Update both branches for the conditional to ensure path sensitivity
            if cond == "=" and value == 0:
                if abstract_vals[var] in ["P", "N"]:
                    # If we reach the false branch, x cannot be zero
                    abstract_vals[var] = "P" if abstract_vals[var] == "P" else "N"
                else:
                    abstract_vals[var] = "T"
                # Add the target of the conditional goto back to the worklist to consider the true branch
                if target not in worklist:
                    worklist.append(target)
                # Also re-add the next instruction to continue false branch exploration
                if (index + 2) <= len(parsed_instructions) and (index + 2) not in worklist:
                    worklist.append(index + 2)

        elif instr.instr_type == "assign_var":
            var1 = instr.details["var1"]
            var2 = instr.details["var2"]
            abstract_vals[var1] = abstract_vals[var2]

        elif instr.instr_type == "binary_op":
            var = instr.details["var"]
            var1 = instr.details["var1"]
            var2 = instr.details["var2"]
            op = instr.details["op"]
            if op == "-":
                # Special handling for subtraction to check if the result could be zero
                if abstract_vals[var1] == "P" and abstract_vals[var2] == "P":
                    abstract_vals[var] = "T"  # Result could be positive or zero
                elif abstract_vals[var1] == "N" and abstract_vals[var2] == "N":
                    abstract_vals[var] = "T"  # Result could be negative or zero
                elif abstract_vals[var1] == "Z" or abstract_vals[var2] == "Z":
                    abstract_vals[var] = "T"  # If either value is zero, the result could be less certain
                else:
                    abstract_vals[var] = "T"

                # Re-add current and all subsequent instructions to the worklist for proper propagation
                for successor in range(index, len(parsed_instructions)):
                    if (successor + 1) not in worklist:
                        worklist.append(successor + 1)
            elif op == "+":
                if abstract_vals[var1] == "P" and abstract_vals[var2] == "P":
                    abstract_vals[var] = "P"
                elif abstract_vals[var1] == "N" and abstract_vals[var2] == "N":
                    abstract_vals[var] = "N"
                elif abstract_vals[var1] == "Z" or abstract_vals[var2] == "Z":
                    # If either value is zero, the result could be less certain
                    abstract_vals[var] = "T"
                else:
                    abstract_vals[var] = "T"
            else:  # Assume * or /
                abstract_vals[var] = "T"  # For simplicity

            # Explicitly re-add all affected instructions to the worklist to ensure propagation
            for successor in range(index, len(parsed_instructions)):
                if (successor + 1) not in worklist:
                    worklist.append(successor + 1)

        elif instr.instr_type == "goto":
            # Ensure we add the target of the goto to the worklist for re-evaluation
            target = instr.details["target"]
            if target not in worklist:
                worklist.append(target)
            # Revisit the goto statement to ensure changes are propagated
            if (index + 1) not in worklist:
                worklist.append(index + 1)

        elif instr.instr_type == "halt":
            # Treat halt as an instruction that stops further propagation and ensures all variables are finalized
            # For simplicity, halt will finalize variables, meaning their values will not be updated further
            worklist.clear()  # Clear the worklist as execution halts here

        if old_vals != abstract_vals:
            # Add successors of the current instruction to the worklist
            for successor in range(index + 1, len(parsed_instructions)):
                if (successor + 1) not in worklist:
                    worklist.append(successor + 1)

        # Print the current state after each iteration
        worklist_str = ', '.join(map(str, worklist)) if worklist else "empty"
        abstract_val_str = ', '.join([f"{k}->{v}" for k, v in abstract_vals.items()])
        print(f"instr | worklist | abstract val\n{iteration} | {worklist_str} | {abstract_val_str}")
        iteration += 1


def reaching_def_analysis(parsed_instructions):

    return

def main():
    # Parse command line arguments
    parser_args = argparse.ArgumentParser(description="Give a W3A file and either signed or reaching for analysis type (ex: python W3A_DataFlow.py prog_1.w3a reaching)")
    parser_args.add_argument("W3A_file", help="Path to the W3A file to analyze.")
    parser_args.add_argument("function", help="Type of flow function, either signed or reaching")
    args = parser_args.parse_args()

    # Parse the file and print the instructions
    parser = Parser(args.W3A_file)
    parsed_instructions = parser.get_instructions()
    print(parsed_instructions)

    lattice = Lattice(args.function)
    #print(lattice.is_less_than_equal("⊥", "T"))  # True

    #for instr in parsed_instructions:
        #print(instr)

    # Create the control flow graph
    cfg = CFG(parsed_instructions)
    #print(f"CFG: {cfg.cfg}")
    # Select the appropriate flow function
    if args.function == "signed":
        flow_function = IntegerSignAnalysisFlowFunction()
        #logging.info("Using Integer Sign Analysis Flow Function")
    elif args.function == "reachability":
        flow_function = VariableReachabilityFlowFunction()
    else:
        raise ValueError(f"Unknown analysis type: {args.function}")
    
    #worklist_object = Worklist(parsed_instructions, lattice, cfg, args.function)
    #worklist_object.run()
    worklist_object = Worklist(parsed_instructions, flow_function)
    # Analyze the program 
    input_states, output_states = worklist_object.analyze()
    print("Final Input States:", input_states) 
    print("Final Output States:", output_states)


    '''if args.function == "signed":
        print("Performing Integer Sign Analysis....")
        int_sign_analysis(parsed_instructions)
    elif args.function == "reaching":
        print("Performing Reaching Definitions Analysis....")
        reaching_def_analysis(parsed_instructions)'''

    return

main()