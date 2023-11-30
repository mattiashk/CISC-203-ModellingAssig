import re
import datalayer
import timetableview
import sat_solver
import requests
import os
import json
import pprint

"""
Contains utility classes and functions for the timetable scheduling SAT solver. 
Includes functionality for initializing test cases, handling web app interactions, 
sharing data with the web app, parsing test case requests and interacting with the
SAT solver to generate solutions.
"""

class TextColor:
    """
    Escape codes for different text colors in the console.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    

class ViewTestCase:
    """
    Represents a test case modeled after the data in test.config.json.

    Attributes:
        id (str): The unique test case id.
        test (str): The name of the test.
        description (str): A description of the test case.
        location (str): The location of the test case data.
    """
    def __init__(self, id, test, description, location):
        self.id = id
        self.test = test
        self.description = description
        self.location = location
    def __str__(self):
        return f"{TextColor.OKGREEN}Id: {TextColor.OKBLUE}{self.id}  {TextColor.HEADER}Name:{TextColor.ENDC} {self.test} {TextColor.HEADER}Description:{TextColor.ENDC} {self.description}"

class AllTestCases:
    """
    A collection of all test cases.

    Attributes:
        ALLTESTIDS (list): A list of all test case IDs.
        ALLTESTS (dict): A dictionary of all test cases.
    """
    ALLTESTIDS = []
    ALLTESTS = None
    
    def __init__(self, cases):
        self.cases = {}
        for case in cases:
            self.cases[case.id] = case

        for case in self.cases.values():
            AllTestCases.ALLTESTIDS.append(case.id) #list of all test ids
            
        AllTestCases.ALLTESTS = self.cases #dict of all tests
    
    def __str__(self):
        formatted_str = ""
        for case in self.cases.values():
            formatted_str += f"{case}\n"
        return formatted_str
    
    def __contains__(self, id):
        return id in self.cases
    


def initalize_test_cases():
    """
    Initializes and returns a collection of test cases read from a the tests.config.json configuration file.

    Returns:
        AllTestCases: An instance of AllTestCases containing all test cases.
    """
    cases = []
    with open('tests.config.json', 'r') as config_file:
        config = json.load(config_file)
        for testcase in config:
            cases.append(ViewTestCase(**testcase))
            
    return AllTestCases(cases)

def get_webapp_preferences():
    """
    Reads and returns the user's preference for using a web app from the config.json configuration file.

    Returns:
        bool: The user's preference for using a web app.
    """
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        
        # Access user preferences
        webapp = config['use_web_app']
        return webapp

def get_console_solution_preferences():
    """
    Reads and returns the user's preference for showing propositions in the console from the config.json configuration file.

    Returns:
        bool: The user's preference for showing propositions in the console.
    """
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        
        # Access user preferences
        webapp = config['show_propositions']
        return webapp

def warn(message):
    """Prints a warning message in red to the console

    Args:
        message (str): the warning message to be printed
    """
     
    red_code = "\033[91m"
    reset_code = "\033[0m"

    # Print the text in red
    print(f"{red_code}WARNING: {message}{reset_code}")

def extract_courses(course_string):
    """
    Extracts course codes from a string using a regular expression.

    Args:
    - course_string (str): The input string containing course codes.

    Returns:
    - list: List of extracted course codes.
    """
    pattern = r'\b[A-Z]{4}-\d{3}\b'
    return re.findall(pattern, course_string)


def display_propositions(sol):
    """
    Pretty prints the solution propositions.

    Args:
        sol (dict): The solution to be printed.
        
    Note: depends on the state of get_console_solution_preferences
    """
    pprint.pprint(sol)

def display_course_selection(sol, objects):
    """
    Displays the course selection for each student based on the provided SAT solution.

    Args:
        sol (dict): The solution containing the course enrollments for all students.
        objects (dict): The datalayer collection objects.
    """
    students = objects["students"]
    for student in students:
        course_collection = {datalayer.Term.FALL: [], datalayer.Term.WINTER: [], datalayer.Term.SUMMER: []}
        for course in student.course_wish_list:
            if sol[sat_solver.StudentEnrolledCourse(student, course)]:
                
                offered_terms = course.sections.get_term_offerings()
                for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                    if sol[sat_solver.StudentEnrolledCourseTerm(student, course, term)]:
                        
                        term_offerings = course.sections.get_term_collection(term)#get course term offerings
                        for section in term_offerings: #get the Section objects from the term_offering
                            if sol[sat_solver.StudentEnrolledCourseSection(student, course, term, section)]:
                                course_collection[term].append(f"{section.courseid}-{section.class_number}")
                                
        print(f"{TextColor.HEADER}{student.name}:{TextColor.ENDC} Has been enrolled in {TextColor.HEADER}Fall:{TextColor.OKBLUE}{course_collection[datalayer.Term.FALL]}{TextColor.ENDC}, {TextColor.HEADER}Winter:{TextColor.OKBLUE}{course_collection[datalayer.Term.WINTER]}{TextColor.ENDC}, {TextColor.HEADER}Summer:{TextColor.OKBLUE}{course_collection[datalayer.Term.SUMMER]}{TextColor.ENDC}")



def display_timetable_view(solution, objects):
    """
    Displays the timetable view in the web app by creating and sharing the solution data.

    Args:
        solution (dict): The solution to be displayed.
    """ 
    data = timetableview.create_json(solution, objects)
    post_data_to_api(data)
    
def post_data_to_api(data):
    url = 'http://localhost:3000/api/recieve-data'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        print("Data posted to web app successfully")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None



def parse_sat_test(test_number):
    """
    Parses and solves a SAT test based on the given test number.

    Args:
        test_number (int): The id of the test to solve.

    Returns:
        dict: A dictionary indicating the status and message of the operation.
    """
    AllTestCases.ALLTESTIDS
    print(f"{TextColor.OKGREEN}Executing {test_number}{TextColor.ENDC}")
    
    if test_number in AllTestCases.ALLTESTIDS:
        result = sat_solve_request(test_number)
        if result != False:
            S = result["Solution"]
            O = result["Objects"]
            display_timetable_view(S, O)
            return {"status": "success", "message": f"Test number: {test_number} parsed"}
        else:
            return {"status": "failure", "message": f"An error occured while executing the sat solver"}
    
    else:
        return {"status": "failure", "message": f"Test number: {test_number} does not exists"}

def sat_solve_request(test_number):
    """
    Requests a solution to a SAT problem based on the given test number.

    Args:
        test_number (int): The test number for which the SAT problem is to be solved.

    Returns:
        dict or bool: The result dictionary containing the solution and objects if successful, or False if an error occurs.
    """
    try:
        if datalayer.data == None or datalayer.testid != test_number:
            objects = create_data_layer(AllTestCases.ALLTESTS[test_number].location)
        else:
            datalayer.data = test_number
            objects = datalayer.data
        result_dict = sat_solver.execute(objects)
        result_dict["Objects"] = objects
        return result_dict
    except Exception as e:
        print(f"{TextColor.FAIL}{e}{TextColor.ENDC}")
        return False
        


def create_data_layer(datalocation="default"):
    """
    Create a data layer by loading the JSON configuration file and mapping data from the files listed in the configuration file.

    This function loads the JSON configuration file, which specifies the file paths
    for courses, buildings, and sections data. It then maps the data from these files
    to corresponding data structures, such as Course, Department, and CourseSection objects,
    using functions provided by the 'datalayer' module.

    Args:
        datalocation (str, optional): The location containing the json. Defaults to "default" and reads location from config.json.

    Returns:
        dict: a dictionary containting the Courses, Departments, Students, Requirements data objects
    """
    
    if datalocation != "default":
        # Access the data file paths
        courses_file_path = os.path.join(datalocation, "courses.json")
        #buildings_file_path = os.path.join(basepath, "buildings.json") #unused
        sections_file_path = os.path.join(datalocation, "sections.json")
        departments_file_path = os.path.join(datalocation, "departments.json")
        students_file_path = os.path.join(datalocation, "students.json")
        requirements_file_path =os.path.join(datalocation, "requirements.json")
        
        
    else:
        # Load the JSON configuration file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        # Access the data file paths
        courses_file_path = config['courses_file']
        #buildings_file_path = config['buildings_file'] #unused
        sections_file_path = config['sections_file']
        departments_file_path = config['departments_file']
        students_file_path = config['students_file']
        requirements_file_path = config['requirements_file']

    #create data set
    all_courses = datalayer.mapCourses(courses_file_path)
    all_sections = datalayer.mapSections(sections_file_path)
    all_students = datalayer.mapStudents(students_file_path)
    all_departments = datalayer.mapDepartments(departments_file_path)
    all_requirements = datalayer.mapRequirements(requirements_file_path)
    
    # Set the Module-level attribute to a dictionary containing all data sets
    data = {"courses": all_courses, "departments": all_departments, "students": all_students, "requirements": all_requirements, "sections": all_sections}
    datalayer.data = data

    return data
