import argparse
from z3 import *
import tree_sitter_c as tsc
from tree_sitter import Language, Parser
import os
import logging



# conditions shouldn't be attached to specific symbolic vars, just left and right sides if left side is an operations do some step.
# need to updated conditions to handle the left side. so X = X+Y doesn't feed the solver X0 = X+Y  should be X0 = X0 + X1 for example.

#Given conditions reached what was the state at that time

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
        self.condition = []
        #self.current_path_condition = BoolVal(True)
        # Stack to save and restore states for branching
        self.saved_states = []
        # Counters to track feasible and infeasible paths
        self.SAT = 0
        self.UnSAT = 0
        # Counter for paths that meet the target condition `return 1;`
        self.targetReached = 0

        self.solver = Solver()

    def save_state(self,next_node):
        logging.info("")
        logging.info(f"Entered save_state with next_node: {next_node}") 
        # Saves the current state by storing the path condition,
        # variable mappings, and counter in the saved states stack.
        state = {
            "conditions": self.condition,
            "mapping": self.mapping.copy(),
            "counter": self.counter,
            "next_state": next_node
            # add next state to execute
        }
        logging.info(f"State: {state}")
        self.saved_states.append(state)
        print("State saved.")

    def restore_state(self):
        # Restores the last saved state, including the path condition,
        # variable mappings, and counter.
        if self.saved_states:
            state = self.saved_states.pop()
            self.condition = state["conditions"]
            self.mapping = state["mapping"]
            self.counter = state["counter"]

            print("State restored.")
            return state["next_state"]

        else:
            print("No saved state to restore.")
        return

    def execute(self, root_node, function):
        # Main entry point to execute the symbolic interpreter on a function
        # Parses all functions from the root node and then begins traversing
        # the specified function node
        self.find_functions(root_node)
        node = self.functions[function]
        self.traverse_node(node)
        # Outputs results on paths after execution
        print("Number of infeasible states:", self.UnSAT)
        print("Number of feasible states:", self.SAT)
        print("Number of Target reached:", self.targetReached)

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

        elif node.type =='update_expression':
            # Handle increment (++) and decrement (--) expressions
            expression_text = node.text.decode('utf-8').strip()  # Get the expression text
            if expression_text.endswith('++'):
                var_name = expression_text[:-2].strip()
                self.condition.append([self.mapping[var_name][-1], '++', '1', False])
            elif expression_text.endswith('--'):
                var_name = expression_text[:-2].strip()
                self.condition.append([self.mapping[var_name][-1], '--', '1', False])
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
        logging.info(f"solver.assertions: {self.solver.assertions()}")

        # Solve the constraints
        result = self.solver.check()
        logging.info(f"Solver result: {result}")
        if result == z3.sat:
            model = self.solver.model()
            logging.info(f"Model: {model}")
            print("SAT")
            print(model)
            logging.info("")
            return model
        elif result == z3.unsat:
            logging.info("UNSAT")
            print("UNSAT")
        else:
            logging.info("UNKNOWN")
            print("UNKNOWN")
        

    
    def z3_condition_add(self, solver, op, left, right,inv):
        # Applies basic operators in Z3 to form a symbolic expression
        # fix
        if op == '+':
            self.solver.add(left =  right)
        elif op == '-':
            self.solver.add(left =  right)
        elif op == '*':
            self.solver.add(left = right)
        elif op == '/':
            self.solver.add(left = right)

        # boolean operators
        elif op == '==':
            if inv:
                self.solver.add(not(left == right))
            else:
                self.solver.add(left == right)
        elif op == '<':
            if inv:
                self.solver.add(not(left<right))
            else:
                self.solver.add(left < right)
        elif op == '>':
            if inv:
                self.solver.add(z3.Not(left>right))
            else:
                self.solver.add(left > right)

        elif op == '=':
            self.solver.add(left == right)
        elif op == '++':
            self.solver.add(Int(left) == Int(left) + 1)
        elif op == '--':
            self.solver.add(Int(left) == Int(left) - 1)
        return



    
    def else_constraints(self, condition,inv): # condition is new_condition
        #solver = Solver()
        #copied_solver = self.solver.translate(self.solver.ctx)

        # Why are we looking at all the mappings?
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
        #self.get_concrete_value()
        logging.info(f"Concret value: {self.get_concrete_value()}")
        '''for m in self.mapping.items():
            logging.info("")
            logging.info(f"Mapping m: {m}")
            logging.info(f"Mapping m[-1]: {m[1]}")
            for sv in m[-1]:
                logging.info(f"Mapping sv: {sv}")
                unique_id = Int(sv)
                logging.info(f"Unique_id: {unique_id}")
                solver.add(Distinct(unique_id)) # add variables to the solver.
                logging.info(f"Added variable to solver: {unique_id}")'''


        # add any previous conditions
        for c in self.condition:
                logging.info("")
                logging.info(f"Condition c: {c}")
                logging.info(f"Condition c[0]: {c[0]}")
                logging.info(f"Condition c[1]: {c[1]}")
                logging.info(f"Condition c[2]: {c[2]}")
                logging.info(f"Condition c[3]: {c[3]}")
                op = c[1]
                right = c[0]
                left = c[2]
                inv = c[3]
                self.z3_condition_add(self.solver, op, left, right,inv)
                logging.info(f"Added condition to solver: {op} {left} {right} {inv}")

        '''logging.info("")
        logging.info("In check_feasibility, misterious condition: ")
        op = condition.children[1].text.decode()
        logging.info(f"Condition op: {op}")
        right = condition.children[0].text.decode()
        logging.info(f"Condition right: {right}")
        left = self.mapping[condition.children[2].text.decode()][-1]
        logging.info(f"Condition left: {left}")
        self.z3_condition_add(solver,op, left, right,inv)
        logging.info(f"Added condition to solver: {op} {left} {right} {inv}")'''

        result = self.solver.check() == sat
        return result



    def check_feasibility(self, condition,inv): # condition is new_condition
        #solver = Solver()
        copied_solver = self.solver.translate(self.solver.ctx)

        # Why are we looking at all the mappings?
        unique_id = Int(self.mapping[condition.children[0].text.decode()][-1])
        copied_solver.add(Distinct(unique_id)) # add variables to the solver.
        logging.info(f"Added variable to solver: {unique_id}")

        op = condition.children[1].text.decode()
        logging.info(f"Condition op: {op}")
        right = unique_id
        logging.info(f"Condition right: {right}")


        unique_id = Int(self.mapping[condition.children[2].text.decode()][-1])
        copied_solver.add(Distinct(unique_id)) # add variables to the solver.
        logging.info(f"Added variable to solver: {unique_id}")
        left = unique_id
        logging.info(f"Condition left: {left}")
        
        self.z3_condition_add(copied_solver, op, left, right,inv)
        logging.info(f"Added condition to solver: {op} {left} {right} {inv}")
        #self.get_concrete_value()
        logging.info(f"Concret value: {self.get_concrete_value()}")
        '''for m in self.mapping.items():
            logging.info("")
            logging.info(f"Mapping m: {m}")
            logging.info(f"Mapping m[-1]: {m[1]}")
            for sv in m[-1]:
                logging.info(f"Mapping sv: {sv}")
                unique_id = Int(sv)
                logging.info(f"Unique_id: {unique_id}")
                solver.add(Distinct(unique_id)) # add variables to the solver.
                logging.info(f"Added variable to solver: {unique_id}")'''


        # add any previous conditions
        '''for c in self.condition:
                logging.info("")
                logging.info(f"Condition c: {c}")
                logging.info(f"Condition c[0]: {c[0]}")
                logging.info(f"Condition c[1]: {c[1]}")
                logging.info(f"Condition c[2]: {c[2]}")
                logging.info(f"Condition c[3]: {c[3]}")
                op = c[1]
                right = c[0]
                left = c[2]
                inv = c[3]
                self.z3_condition_add(copied_solver, op, left, right,inv)
                logging.info(f"Added condition to solver: {op} {left} {right} {inv}")'''

        '''logging.info("")
        logging.info("In check_feasibility, misterious condition: ")
        op = condition.children[1].text.decode()
        logging.info(f"Condition op: {op}")
        right = condition.children[0].text.decode()
        logging.info(f"Condition right: {right}")
        left = self.mapping[condition.children[2].text.decode()][-1]
        logging.info(f"Condition left: {left}")
        self.z3_condition_add(solver,op, left, right,inv)
        logging.info(f"Added condition to solver: {op} {left} {right} {inv}")'''

        result = self.solver.check() == sat
        if result == sat:
            logging.info("Feasible")
            self.solver = copied_solver
        return result

    def handle_declaration(self, node):
        logging.info("")
        logging.info(f"Handling declaration: {node.text.decode()}")
        # Just getting the values
        dNode = node.child_by_field_name('declarator')
        logging.info(f"Declarator node: {dNode.text.decode()}")

        # Generates a unique identifier for the symbolic variable
        symbolic_var = f'X{self.counter}'
        self.counter += 1  # add to counter so ids are unique.

        if not dNode.children:
            logging.info(f"dNode.children: {dNode.children}")
            # create a mapping for example int x: x->X1
            # Initialize the stack for this variable if it doesn't exist
            #logging.info(f"Check if mapping exist{self.mapping[dNode.text.decode()]}")
            self.mapping[dNode.text.decode()] = []
            # Append the new assignment to the list (stack behavior)
            self.mapping[dNode.text.decode()].append(symbolic_var)
            print(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")
        else:
            logging.info(f"dNode.children: {dNode.children}")
            # x1-> c[[X1,<,10,False],[X1 = 10]]
            var_name = dNode.children[0].text.decode()
            logging.info(f"var_name: {var_name}")
            # Initialize the stack for this variable if it doesn't exist
            self.mapping[var_name] = []
            # Append the new assignment to the list (stack behavior)
            self.mapping[var_name].append(symbolic_var)
            logging.info(f"Mapping: {self.mapping}")

            left = dNode.children[2]
            if left.type == 'call_expression':
                logging.info(f"Left: {left.text.decode()}")
                # this is a function, and we just want this symbolic var to be a generic Int to the solver
                # later when we feed the mappings to the solver this will happen (Int(symbolic_var))
                print(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")
                pass

            else:
                logging.info(f"Left: {left.text.decode()}")
                # conditions, operator, right and left side of the variable
                op = dNode.children[1].text.decode()
                logging.info(f"Op: {op}")
                right = self.mapping[dNode.children[0].text.decode()][-1] # we decide later how to handle this side
                logging.info(f"Right: {right}")
                inv = False  # for not conditions only with boolean operators.
                #logging.info(f"self.mapping[left.text.decode()]: {self.mapping[right][-1]}")  
                left_key = left.text.decode()
                if left_key in self.mapping:
                    logging.info(f"type of: {type(self.mapping[left_key][-1])}")
                else:
                    logging.error(f"Key {left_key} not found in mapping")
                self.condition.append([op, right, left, inv])
                print(f" {dNode.text.decode()} mapped to {symbolic_var}")
            logging.info(f"Declared variable {dNode.text.decode()} mapped to {symbolic_var}")

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
            # conditions, operator, right and left side of the variable
            op = node.children[1].text.decode()
            right = node.children[0].text.decode()
            left = node.children[2].text.decode()
            inv = False  # for not conditions only with boolean operators.
            self.condition.append([op, right, self.mapping[left][-1], inv])
            print(f"Assigned {var_name} = {node} ")
        else:
            print(f"{var_name} assinging value that hasn't been defined")
        logging.info(f"Assigned {var_name} = {symbolic_var}")
        # log the contents of conditions list
        logging.info(f"Conditions: {self.condition}")

    def handle_if_statement(self, node):
        logging.info("")
        logging.info(f"Handling if statement: {node.text.decode()}")
        # Handles if statements by creating branches for true and false conditions
        condition_node = node.child_by_field_name('condition')
        logging.info(f"Condition_node: {condition_node.text.decode()}")
        true_branch = node.child_by_field_name('consequence')
        logging.info(f"True_branch: {true_branch.text.decode()}")
        false_branch = node.child_by_field_name('alternative')
        logging.info(f"False_branch: {false_branch.text.decode()}")

        new_condition = condition_node.children[1]
        logging.info(f"New_condition: {new_condition.text.decode()}")

        #logging.info(f"new_condition feasible: {self.check_feasibility(new_condition,False)}")
        logging.info("Why are we checking the feasibility for the new condition?")

        ### Why are we checking the feasibility for the new condition?
        if self.check_feasibility(new_condition,False):
            # add the new condition to the branches
            op = new_condition.children[1].text.decode()
            right = self.mapping[new_condition.children[0].text.decode()][-1]
            left = self.mapping[new_condition.children[2].text.decode()][-1]
            self.condition.append([right,op,left,False])

            print("if statement", new_condition.text.decode())
            self.SAT += 1  # satisfiable condition
            logging.info("")
            logging.info(f"node.next_sibling: {node.next_sibling}. Will call save_state")
            self.save_state(node.next_sibling)  # save the state and then traverse this branch
            logging.info(f"Will call traverse_node with true_branch")
            self.traverse_node(true_branch)
        else:
            self.UnSAT += 1

            if (false_branch is not None):
                logging.info("")
                logging.info("False branch exists")
                logging.info(f"False branch: {false_branch.text.decode()}") # Contains the else block
                # False branch feasibility check and traversal if feasible
                logging.info("checks feasibility for the new condition INVERSE")
                self.else_constraints(new_condition,True)
                print("Else statement", new_condition.text.decode())
                # add the new condition to the branches
                op = new_condition.children[1].text.decode()
                right = self.mapping[new_condition.children[0].text.decode()][-1] # get symbolic var at this point
                left = self.mapping[new_condition.children[2].text.decode()][-1]  # get symbolic var at this point
                self.condition.append([right, op, left, True])

                self.save_state(node.next_sibling)
                self.traverse_node(false_branch)
                self.SAT += 1

            #else:
                #self.UnSAT += 1
        return

    def handle_while_statement(self, node):
        # Handles while loops by repeatedly checking loop condition feasibility
        # and traversing the loop body as long as the condition holds
        condition_node = node.child_by_field_name('condition').children[1]
        body_node = node.child_by_field_name('body')
        self.save_state(node.next_sibling)
        while True:

            if self.check_feasibility(condition_node,False):

                print("Loop condition is SAT, continuing")
                self.traverse_node(body_node)  # while it's feasible traverse the node when the nodes done we should go back
                self.SAT = self.SAT +1
            else:
                print("Loop condition is UNSAT, breaking")
                self.UnSAT = self.UnSAT + 1
                self.restore_state()  # if it wasn't feasible, we want to pop the state we just added
                break


        return

    def handle_return(self, node):
        logging.info(f"Handling return statement: {node.text.decode()}")
        logging.info(f"Node.children: {node.children[1]}") 
        number_literal_node = node.children[1]
        number_literal_value = int(number_literal_node.text.decode())
        logging.info(f"Number_literal_value: {number_literal_value}")
        # Processes return statements, checking if they meet the target condition
        #return_value_node = node.child_by_field_name('value')
        #logging.info(f"Return_value_node: {return_value_node.text.decode()}")
        #if return_value_node is not None:
            #return_value = return_value_node
        if number_literal_value == IntVal(1):
            # Increments target counter if the return value matches target
            self.targetReached += 1
            print("Target reached!")

        else:
            print("Non-target return reached")
        self.restore_state()
        return # go back to the last branch


def main():
    # I am lazy and don't want to run from the command line everytime, un comment out later.
    # parser_args = argparse.ArgumentParser(description="Parse a C file using Tree-sitter.")
    # parser_args.add_argument("c_file", help="Path to the C file to parse.")
    # parser_args.add_argument("function",help="Function to symbolically execute")

    # args = parser_args.parse_args()
    ## Read C code from the file
    # c_code = read_c_code_from_file(args.c_file)

    # Get file path to the c file in question.
    current_directory = os.getcwd()
    file_name = "test_program.c"
    file_path = os.path.join(current_directory, file_name)

    # read in c code
    c_code = read_c_code_from_file(file_path)

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

