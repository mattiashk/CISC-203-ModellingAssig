
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

import datalayer
import main #TODO needs to be removed and code needs to be added to build_theorey

"""
    This python file

    Returns:
        None

    Example:
"""

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class StudentEnrolled(Hashable): #has a section
    def __init__(self, student, course, term, course_section):
        self.student = student #a Student object
        self.course = course #parent object of the section
        self.term = term
        self.section = course_section

    def __repr__(self):
        return f"({str(self.student.name)} in {str(self.course.id)} T: {str(self.term)} -> {str(self.section.class_number)})"

@proposition(E)
class StudentCourse(Hashable): #not section i.e, generalized
    def __init__(self, student, course, term):
        self.student = student #a Student object
        self.course = course #parent object of the section
        self.term = term

    def __repr__(self):
            return f"({str(self.student.name)} in {str(self.course)} T: {str(self.term)}"

def build_propositions():
    #Build Propositions
    objects = main.create_data_layer()
    students = objects["students"]

    student_enrolled = []
    for student in students:
        for course in student.courses:
            for term in course.section: #loop over "Winter", "Summer", "Fall" if they exist for this specific course
                for course_section in course.section[term].course_sections: #loop over each course section "001", "002" for this specific course
                    student_enrolled.append(StudentEnrolled(student, course, term, course_section))

    #For every student and course, they can only be enrolled in a course during one of "Summer", "Winter", "Fall" depending on the courses offering 
    for student in students:
        for course in student.courses:
            term_options = [] #all possible term options for a specifc course ex: "Fall", "Winter", "Summer"
            for term in course.section: #loop over "Winter", "Summer", "Fall" if they exist for this specific course
                coursecode = course.section[term].courseid
                term_options.append(StudentCourse(student, coursecode, term))

def build_theory():
    """
    #TODO
    """
    #Build Propositions
    objects = main.create_data_layer()
    students = objects["students"]

    build_propositions()

    
    #For every student and course, they can be enrolled in exactly one section of a course 
    for student in students:
        for course in student.courses:
            for term in course.section: #loop over "Winter", "Summer", "Fall" if they exist for this specific course
                section_options = [] #all possible section options for a specifc course during a specific term ex: "CISC-204-001", "CISC-204-002" During the "Winter" term
                for course_section in course.section[term].course_sections: #loop over each course section "001", "002" for this specific course
                    section_options.append(StudentEnrolled(student, course, term, course_section))

                #For every student and course, they can be enrolled in exactly one section of a course 
                constraint.add_exactly_one(E, section_options)

    #For every student and course, they can only be enrolled in a course during one of "Summer", "Winter", "Fall" depending on the courses offering 
    for student in students:
        for course in student.courses:
            term_options = [] #all possible term options for a specifc course ex: "Fall", "Winter", "Summer"
            for term in course.section: #loop over "Winter", "Summer", "Fall" if they exist for this specific course
                coursecode = course.section[term].courseid
                term_options.append(StudentCourse(student, coursecode, term))

            #For every student and course, they can be enrolled in the course during only one term ex: one of "Fall", "Winter", "Summer" depending on a courses offering
            constraint.add_exactly_one(E, term_options)


    #For every student and course, if they are not taking the course during a term they should not be enrolled in any of its sections
    for student in students:
        for course in student.courses:
            for term in course.section: #loop over "Winter", "Summer", "Fall" if they exist for this specific course
                for course_section in course.section[term].course_sections: #loop over each course section "001", "002" for this specific course
                    pass #E.add_constraint(~StudentCourse(student, course.section[term].courseid, term) >> ~StudentEnrolled(student, course, term, course_section))
    return E
                

def display_solution(sol):
    import pprint
    pprint.pprint(sol)
    #display_assignment(sol)
    #display_student_prefs(sol)


if __name__ == "__main__":
    T = build_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution:")
    sol = T.solve()

    display_solution(sol)
