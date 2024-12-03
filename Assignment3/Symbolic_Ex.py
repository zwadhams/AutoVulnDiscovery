import argparse
from z3 import *
import tree_sitter_c as tsc
from tree_sitter import Language, Parser
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

C_LANG = Language(tsc.language())
parser = Parser(C_LANG)

# Example path: Assignment3\test_program.c
def read_c_code_from_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def print_tree(node, indent=""):
    hold = f"{indent}{node.type} "  # [{node.start_point}, {node.end_point}]
    print(hold)
    for child in node.children:
        print_tree(child, indent + "  ")
    return

class SymbolicExecutor:
    def __init__(self):
        # Dictionary to store function nodes, allowing for function calls
        self.functions = {}
        # Maps variable names to their SymbolicVariable instances
        self.mapping = {}
        # Counter for generating unique variable identifiers
        self.counter = 0
        # Counters to track feasible and infeasible paths
        self.SAT = 0
        self.UnSAT = 0
        # Counter for paths that meet the target condition `return 1;`
        self.targetReached = 0
        self.solver = Solver()
        self.while_condition = False
    

    def execute(self, root_node, function):
        # Main entry point to execute the symbolic interpreter on a function
        # Parses all functions from the root node and then begins traversing
        # the specified function node
        self.find_functions(root_node)
        node = self.functions[function]
        self.traverse_node(node)
        # Outputs results on paths after execution
        print("Number of infeasible states:", self.UnSAT)
        logging.info(f"Number of infeasible states: {self.UnSAT}")
        print("Number of feasible states:", self.SAT)
        logging.info(f"Number of feasible states: {self.SAT}")
        print("Number of Target reached:", self.targetReached)
        logging.info(f"Number of Target reached: {self.targetReached}")

    def find_functions(self, node):
        # Recursive function to locate and store all function definitions
        # within the code tree. Assumes function name is the first child node.
        if node.type == 'function_definition':
            declarator_node = node.child_by_field_name('declarator')
            function_name_node = declarator_node.children[0]
            function_name = function_name_node.text.decode('utf-8')
            self.functions[function_name] = node
            print("Function found:", function_name)
        for child in node.children:
            self.find_functions(child)

    def traverse_node(self, node):
        # Traverses each node type in the function body and delegates handling
        # of specific node types to helper methods based on functionality
        logging.info("")
        logging.info(f"Traversing node: {node.type}")
        if node is None:
            return
        
        if True:
            if node.type =='update_expression':
                    expression_text = node.text.decode('utf-8').strip()  # Get the expression text
                    logging.info(f"Expression text type: {type(expression_text)}")
                    logging.info(f"Expression text: {expression_text}")
                    logging.info(f"Node is: {node.id}")

                    if expression_text.endswith('++') or expression_text.startswith('++'):
                        if expression_text.startswith('++'):
                            logging.info(f"Expression text starts with ++")
                            var_name = expression_text[-1].strip()
                        else:
                            logging.info(f"Expression text ends with ++")
                            var_name = expression_text[:-2].strip()
                        logging.info(f"mapping[Var name][-1]: {self.mapping[var_name][-1]}")
                        
                        current_id = Int(self.mapping[var_name][-1])
                        self.solver.add(Distinct(current_id))  # Add the variable to the solver.
                        self.increment_assignment(var_name)
                        new_current_id = Int(self.mapping[var_name][-1])
                        self.solver.add(Distinct(new_current_id))  # Add the variable to the solver.
                        self.solver.add(new_current_id == current_id + 1)
                        logging.info(f"Added condition to solver: {new_current_id} == {current_id} + 1")
                        node = node.next_sibling  # want to skip ahead, the inside of this "traverse" has been handled in the if function
                        logging.info(f"Node is: {node.id}")
                    elif expression_text.endswith('--') or expression_text.startswith('--'):
                        if expression_text.startswith('--'):
                            logging.info(f"Expression text starts with --")
                            var_name = expression_text[-1].strip()
                        else:
                            logging.info(f"Expression text ends with --")
                            var_name = expression_text[:-2].strip()
                        current_id = Int(self.mapping[var_name][-1])
                        self.solver.add(Distinct(current_id))  # Add the variable to the solver.
                        self.increment_assignment(var_name)
                        new_current_id = Int(self.mapping[var_name][-1])
                        self.solver.add(Distinct(new_current_id))  # Add the variable to the solver.
                        self.solver.add(new_current_id == current_id - 1)
                        logging.info(f"Added condition to solver: {new_current_id} == {current_id} - 1")
                        node = node.next_sibling
                        logging.info(f"Node is: {node.id}")
                    # Log the current state of mapping 
                    logging.info(f"mapping: {self.mapping}")
            elif (node.type == 'declaration') or (node.type =='parameter_declaration'):
                # Declaration node for new variable declarations
                self.handle_declaration(node)
            elif node.type == 'assignment_expression':
                # Assignment node for updating variable values
                self.handle_assignment(node)
            elif node.type == 'if_statement':
                # Conditional branching also we traverse nodes in here, so the next node should be the end of the if statement here
                self.handle_if_statement(node)
                node = node.next_sibling # want to skip ahead, the inside of this "traverse" has been handled in the if function
            elif node.type == 'while_statement':
                self.handle_while_statement(node)
                node = node.next_sibling  # want to skip ahead, the inside of this "traverse" has been handled in the while function
            elif node.type == 'return_statement':
                self.handle_return(node)
            else:
                pass
        # Recursively traverses child nodes
        for child in node.children:
            self.traverse_node(child)


    def get_concrete_value(self):
        logging.info("")
        # Solve the constraints
        result = self.solver.check()
        if result == z3.sat:
            model = self.solver.model()
            print(f"Model eval x: {model.eval(Int(self.mapping['x'][-1]))}")
            print(f"Model eval y: {model.eval(Int(self.mapping['y'][-1]))}")
            logging.info(f"Model eval x: {model.eval(Int(self.mapping['x'][-1]))}")
            logging.info(f"Model eval y: {model.eval(Int(self.mapping['y'][-1]))}")
            return model
        elif result == z3.unsat:
            logging.info("UNSAT")
            print("UNSAT")
        else:
            logging.info("UNKNOWN")
            print("UNKNOWN")
        

    
    def z3_condition_add(self, solver, op, left, right,inv):
        logging.info("")
        #logging.info(f"solver.assertions: {solver.assertions()}")
        logging.info(f"Entered z3_condition_add with op: {op}, left: {left}, right: {right}, inv: {inv}")
        # Applies basic operators in Z3 to form a symbolic expression
        if op == '+':
            solver.add(left =  right)
        elif op == '-':
            solver.add(left =  right)
        elif op == '*':
            solver.add(left = right)
        elif op == '/':
            solver.add(left = right)

        # boolean operators
        elif op == '==':
            if inv:
                solver.add(z3.Not(left==right))
            else:
                solver.add(left == right)
        elif op == '<':
            if inv:
                solver.add(left>=right)
            else:
                solver.add(left < right)
        elif op == '>':
            if inv:
                solver.add(left<=right)
            else:
                solver.add(left > right)
        elif op == '>=':

            if inv:
                solver.add(left<right)
            else:
                solver.add(left >= right)
        elif op == '<=':

            if inv:
                solver.add(left > right)
            else:
                solver.add(left <= right)


        elif op == '=':                
            solver.add(left == right)
        
        return



    
    def else_constraints(self, condition,inv): # condition is new_condition
        unique_id = Int(self.mapping[condition.children[0].text.decode()][-1])
        self.solver.add(Distinct(unique_id)) # add variables to the solver.
        logging.info(f"Added variable to solver: {unique_id}")

        op = condition.children[1].text.decode()
        logging.info(f"Condition op: {op}")
        right = unique_id
        logging.info(f"Condition right: {right}")

        unique_id = Int(self.mapping[condition.children[2].text.decode()][-1])
        self.solver.add(Distinct(unique_id)) # add variables to the solver.
        
        logging.info(f"Added variable to solver: {unique_id}")
        left = unique_id
        logging.info(f"Condition left: {left}")
        
        self.z3_condition_add(self.solver, op, left, right,inv)
        logging.info(f"Added condition to solver: {op} {left} {right} {inv}")

        result = self.solver.check() == sat
        
        return result



    def check_feasibility(self, condition,inv): # condition is new_condition
        copied_solver = self.solver.translate(self.solver.ctx)

        unique_id = Int(self.mapping[condition.children[0].text.decode()][-1])
        copied_solver.add(Distinct(unique_id)) # add variables to the solver.
        logging.info(f"Added variable to solver: {unique_id}")

        op = condition.children[1].text.decode()
        logging.info(f"Condition op: {op}")
        left = unique_id
        logging.info(f"Condition left: {left}")

        if condition.children[2].type == "number_literal":
            right = condition.children[2].text.decode()
        else:
            right = Int(self.mapping[condition.children[2].text.decode()][-1])
            copied_solver.add(Distinct(right))
        
        logging.info(f"Added variable to solver: {unique_id}")
        logging.info(f"Condition right: {right}")
        
        self.z3_condition_add(copied_solver, op, left, right,inv)
        logging.info(f"Added condition to copied solver: {op} {left} {right} {inv}")

        result = copied_solver.check()
        logging.info(f"copied_solver result: {result}")
        if result == sat and self.while_condition == False:
            logging.info("Feasible")
            print("Feasible")
            self.solver = copied_solver
            self.SAT += 1
        elif result != sat:
            logging.info("Infeasible")
            print("Infeasible")
            self.UnSAT += 1
        return result

    def handle_declaration(self, node):
        dNode = node.child_by_field_name('declarator')
        logging.info(f"Declarator node: {dNode.text.decode()}")

        # Generates a unique identifier for the symbolic variable
        symbolic_var = f'X{self.counter}'
        self.counter += 1  # add to counter so ids are unique.

        if not dNode.children:
            logging.info(f"dNode.children: {dNode.children}")
            self.mapping[dNode.text.decode()] = []
            # Append the new assignment to the list (stack behavior)
            self.mapping[dNode.text.decode()].append(symbolic_var)
            print(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")
            logging.info(f"Mapping: {self.mapping}")
        else:
            logging.info(f"dNode.children: {dNode.children}")
            var_name = dNode.children[0].text.decode()
            logging.info(f"var_name: {var_name}")
            
            if var_name not in self.mapping:
                self.mapping[var_name] = []
            self.mapping[var_name].append(symbolic_var)
            logging.info(f"Mapping: {self.mapping}")

            right = dNode.children[2]
            if right.type == 'call_expression':
                logging.info(f"Right: {right.text.decode()}")
                print(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")
                pass

            else:
                logging.info(f"Left: {right.text.decode()}")
                op = dNode.children[1].text.decode()
                logging.info(f"Op: {op}")
                left = Int(self.mapping[dNode.children[0].text.decode()][-1]) 
                logging.info(f"Right: {right}")
                inv = False
                if right.type == "number_literal":
                    right_c = int(right.text.decode())
                else:
                    right_c = Int(self.mapping[dNode.children[2].text.decode()][-1])
                self.solver.add(left == right_c)
                right_key = right.text.decode()
                if right_key in self.mapping:
                    logging.info(f"type of: {type(self.mapping[right_key][-1])}")
                else:
                    logging.error(f"Key {right_key} not found in mapping")
                print(f" {dNode.text.decode()} mapped to {symbolic_var}")
            logging.info(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")

    
    def increment_assignment(self, var_name):
        logging.info("")
        logging.info(f"Handling increment assignment: {var_name}")
        if var_name in self.mapping:  
            # Generates a unique identifier for the symbolic variable
            symbolic_var = f'X{self.counter}'
            self.counter += 1  # add to counter so ids are unique.
            self.mapping[var_name].append(symbolic_var)
        else:
            print(f"{var_name} assinging value that hasn't been defined")
        logging.info(f"Assigned {var_name} = {symbolic_var}")
    
    def handle_assignment(self, node):
        # should only occur when x = something new
        # Updates a variable with a new condition
        logging.info("")
        logging.info(f"Handling assignment: {node.text.decode()}")
        var_name = node.child_by_field_name('left').text.decode()
        if var_name in self.mapping:  
            # Generates a unique identifier for the symbolic variable
            symbolic_var = f'X{self.counter}'
            self.counter += 1  # add to counter so ids are unique.
            self.mapping[var_name].append(symbolic_var)
            print(f"Assigned {var_name} = {node} ")
            right = node.children[2]
            left = Int(self.mapping[node.children[0].text.decode()][-1])
            if right.type == "number_literal":
                right = int(right.text.decode())
            else:
                right = Int(self.mapping[node.children[2].text.decode()][-1])
            self.solver.add(left == right)
        else:
            print(f"{var_name} assinging value that hasn't been defined")
        logging.info(f"Assigned {var_name} = {symbolic_var}")

    def handle_if_statement(self, node):
        logging.info("")
        logging.info(f"Handling if statement: {node.text.decode()}")
        # Handles if statements by creating branches for true and false conditions
        condition_node = node.child_by_field_name('condition')
        logging.info(f"Condition_node: {condition_node.text.decode()}")
        true_branch = node.child_by_field_name('consequence')
        logging.info(f"True_branch: {true_branch.text.decode()}")
        false_branch = node.child_by_field_name('alternative')
        #logging.info(f"False_branch: {false_branch.text.decode()}")

        new_condition = condition_node.children[1]
        logging.info(f"New_condition: {new_condition.text.decode()}")

        if self.check_feasibility(new_condition,False) == sat:
            print("if statement", new_condition.text.decode())
            self.traverse_node(true_branch)
        else:
            pass

        if (false_branch is not None):
            logging.info("")
            logging.info("False branch exists")
            logging.info(f"False branch: {false_branch.text.decode()}") # Contains the else block
            # False branch feasibility check and traversal if feasible
            logging.info("checks feasibility for the new condition INVERSE")
            self.else_constraints(new_condition,True)
            print("Else statement", new_condition.text.decode())
            self.traverse_node(false_branch)
        else:
            pass
        return

    def handle_while_statement(self, node):
        # Handles while loops by repeatedly checking loop condition feasibility
        # and traversing the loop body as long as the condition holds
        condition_node = node.child_by_field_name('condition').children[1]
        body_node = node.child_by_field_name('body')
        while True:
            if self.check_feasibility(condition_node,False) == sat:
                if not self.while_condition:
                    self.SAT = self.SAT +1
                    self.while_condition = True
                print("Loop condition is SAT, continuing")
                self.traverse_node(body_node)  # while it's feasible traverse the node when the nodes done we should go back
            else:
                print("Loop condition is UNSAT, breaking")
                self.while_condition = False
                break

        return

    def handle_return(self, node):
        logging.info(f"Handling return statement: {node.text.decode()}")
        logging.info(f"Node.children: {node.children[1]}") 
        number_literal_node = node.children[1]
        number_literal_value = int(number_literal_node.text.decode())
        logging.info(f"Number_literal_value: {number_literal_value}")
        
        if number_literal_value == IntVal(1):
            # Increments target counter if the return value matches target
            self.targetReached += 1
            print("Target reached!")
            self.get_concrete_value()

        else:
            print("Non-target return reached")
        
        return # go back to the last branch


def main():
    parser_args = argparse.ArgumentParser(description="Parse a C file using Tree-sitter.")
    parser_args.add_argument("c_file", help="Path to the C file to parse.")
    parser_args.add_argument("function",help="Function to symbolically execute")

    args = parser_args.parse_args()
    # Read C code from the file
    c_code = read_c_code_from_file(args.c_file)

    # parse the code using tree sitter
    tree = parser.parse(c_code)

    # printing out the tree
    root_node = tree.root_node
    #print_tree(root_node)
    # function_to_execute = args.function
    function_to_execute = 'test'
    executor = SymbolicExecutor()
    executor.execute(root_node, function_to_execute)
    executor.get_concrete_value()

    print("done")
    return

main()