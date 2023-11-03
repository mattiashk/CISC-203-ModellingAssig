import json
import datalayer

"""
This Python file initalizes the data layer that is needed.
It should be merged at the top of run.py 

Author: [Hayden Jenkins]
Date: [28/10/23]
"""

def create_data_layer():
    """
    Create a data layer by loading the JSON configuration file and mapping data from the files listed in the configuration file.

    This function loads the JSON configuration file, which specifies the file paths
    for courses, buildings, and sections data. It then maps the data from these files
    to corresponding data structures, such as Course, Department, and CourseSection objects,
    using functions provided by the 'datalayer' module.

    Returns:
        None

    Example:
        create_data_layer()
    """
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

    #Test Cases
    #print(all_students.find_student_by_name("Hayden").course_wish_list.find_course_by_id("CISC-203").description)
    #print(all_students.find_student_by_name("Hayden").course_wish_list)
    #print(all_students.find_student_by_name("Hayden").course_wish_list.find_course_by_id("CISC-204").sections)


    return {"courses": all_courses, "departments": all_departments, "students": all_students, "requirements": all_requirements}


if __name__ == "__main__":
    print("...loading data")
    create_data_layer()
    print("Finished loading data")