
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from bauhaus import Encoding, proposition, constraint, Or, And

import json
import datalayer
import os
import sat_solver
import utils
import threading
import webapp_api
import time
from utils import TextColor

"""
Initalizes and manages the data layer that is needed for the timetable scheduling SAT solver.
It also contains function to run the main program in different modes depending on a users preference, such as web interface or the console mode.
"""

def start():
    """
    Starts the scheduling application. This function initializes the test cases, 
    checks user preferences for web app mode or console mode, and starts required dependencies
    based on the selected mode chosen (web app or console mode).
    """
    # Initialize Test Cases
    testcases = utils.initalize_test_cases()
    
    # Get Web App Preferences
    webapp = utils.get_webapp_preferences()
    
    # If web app is set to true itilialize an HTTP server for communication
    if webapp:
        webapp_api.run_app() #create a flask_thread for the HTTP socket, allows communication with the web app
        
    # Otherwise run the sat solver and to the output the terminal
    else:
        normal_mode(testcases) #run the sat solver and output to terminal

def get_input(cases, invalid_input=None):
    """
    Prompts the user to enter a test case ID or 'e' to exit.
    Validates the input and returns the test case ID if valid.
    If Invalid, the function recursively calls itself until a valid input is provided or the user chooses to exit.

    Args:
        cases (AllTestCases): A AllTestCases collection contating all available test case IDs for selection.
        invalid_input (str, optional): The previously entered invalid input, if provided, an error message is displayed.

    Returns:
        int or bool: Returns the integer test case ID if a valid ID is entered, or False if the user enters 'e' to exit.
    """

    # Prepare the prompt message
    if invalid_input is not None:
        prompt_message = f"{TextColor.FAIL}Invalid input '{invalid_input}'. Please enter a valid test case id or 'e' to exit: {TextColor.ENDC}"
    else:
        # Display available test case IDs
        print(cases)
        prompt_message = f"{TextColor.WARNING}Please enter a test case id from the above list {TextColor.FAIL}or e to exit:{TextColor.ENDC} "
    
    # Prompt for input
    test = input(prompt_message)

    # Check for exit condition
    if test.lower() == 'e':
        return False

    # Check for valid numeric input and convert to integer
    if test.isdigit() and int(test) in utils.AllTestCases.ALLTESTIDS:
        print(f"{TextColor.OKGREEN}Executing test case: {test} {TextColor.ENDC}")

        return int(test)
    else:
        # If input is not valid, recursively call get_input with the invalid input
        return get_input(cases, invalid_input=test)

def normal_mode(cases):
    """
    Runs the application in normal mode. Outputs SAT Solver results to the terminal.

    Args:
        cases (AllTestCases): A collection of test cases as a AllTestCases object, that are to be processed.
    """
    print(f"{TextColor.OKGREEN}Welcome to the Schedule Sensi!{TextColor.ENDC}")
    
    C = True
    count = 0
    while C:
        count += 1
        if count > 1:
            print("--------------------------------------------------------------------------------------------------------------")
            time.sleep(2)
        test_case = get_input(cases)
        
        if test_case is False:
            break
    
        result = utils.sat_solve_request(test_case)
        if  result != None and result != False and result["Solution"] is not None:
            T = result["Theory"]
            S = result["Solution"]
            O = result["Objects"]
            
            if utils.get_console_solution_preferences():
                utils.display_propositions(S)#show all propositions
            
            print("\n")
            print("Satisfiable: %s" % T.satisfiable())
            print("# Solutions: %d" % count_solutions(T))
            if count_solutions(T) != 0:
                print("   Solution:")
                print("\n")
                utils.display_course_selection(S, O)
                print("\n")

        elif result != None and result != False and result["Solution"] is None:
            print(f"{TextColor.FAIL}No Solutions{TextColor.ENDC}")
            print("\n")
        
        else:
            print(f"{TextColor.FAIL}An error occured while executing the sat solver{TextColor.ENDC}")
            print("\n")

        count += 1

def populate_data():
    """
    Populates the web app with a predefined solution
    """
    objects = utils.create_data_layer("data/testing/test-small-general")
    result_dict = sat_solver.execute(objects)
    T = result_dict["Theory"]
    S = result_dict["Solution"]
    utils.display_timetable_view(S, objects) #format solution data and POST to nextjs app

def web_app_mode():
    """
    Runs the application in web app mode. Posts SAT Solver solutions to the Next.js web app.
    """
    populate_data()

def dev_mode():
    """
    Runs the application in a development mode for testing and debugging. Uses a predefined test case.
    """
    # Initialize Test Cases
    cases = utils.initalize_test_cases()
    
    C = True
    count = 0
    while C:
        count += 1
        if count > 1:
            print("--------------------------------------------------------------------------------------------------------------")
            time.sleep(2)
        test_case = get_input(cases)
        
        if test_case is False:
            break
    
        result = utils.sat_solve_request(test_case)

        ##TESTING
        import pprint
        print("Objects:")
        if result != False:
            for key in result["Objects"].keys():
                print(f"{key}: {result['Objects'][key]}")

            print(result["Objects"]["students"]['Student1'].completed_courses)
                
            print("\n")
        

        if  result != None and result != False and result["Solution"] is not None:
            T = result["Theory"]
            S = result["Solution"]
            O = result["Objects"]
            
            
            if utils.get_console_solution_preferences():
                utils.display_propositions(S)#show all propositions
            
            print("\n")
            print("Satisfiable: %s" % T.satisfiable())
            print("# Solutions: %d" % count_solutions(T))
            if count_solutions(T) != 0:
                print("   Solution:")
                print("\n")
                utils.display_course_selection(S, O)
                print("\n")

        elif result != None and result != False and result["Solution"] is None:
            print(f"{TextColor.FAIL}No Solutions{TextColor.ENDC}")
            print("\n")
        
        else:
            print(f"{TextColor.FAIL}An error occured while executing the sat solver{TextColor.ENDC}")
            print("\n")

        count += 1

        C = False

    

    

if __name__ == "__main__":
    start()