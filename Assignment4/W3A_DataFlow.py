import argparse
from parser import Parser
from worklist import Worklist
from sign_analysis_flow_function import IntegerSignAnalysisFlowFunction
from reachability_flow_function import VariableReachabilityFlowFunction
from definitions import DefinitionExtractor

def main():
    # Parse command line arguments
    parser_args = argparse.ArgumentParser(description="Give a W3A file and either signed or reaching for analysis type (ex: python W3A_DataFlow.py prog_1.w3a reaching)")
    parser_args.add_argument("function", help="Type of flow function, either signed or reaching")
    parser_args.add_argument("W3A_file", help="Path to the W3A file to analyze.")
    args = parser_args.parse_args()

    # Parse the file and print the instructions
    parser = Parser(args.W3A_file)
    parsed_instructions = parser.get_instructions()
    
    # Get the definition of the program
    definition_extractor = DefinitionExtractor(parsed_instructions)
    # Select the appropriate flow function
    if args.function == "signed":
        flow_function = IntegerSignAnalysisFlowFunction()
    elif args.function == "reachability":
        flow_function = VariableReachabilityFlowFunction(definition_extractor.definitions)
    else:
        raise ValueError(f"Unknown analysis type: {args.function}")
    
    w3a_file_name = args.W3A_file.replace('.w3a', '')
    worklist_object = Worklist(parsed_instructions, flow_function, args.function, w3a_file_name)
    # Analyze the program 
    worklist_object.analyze()

    return

main()