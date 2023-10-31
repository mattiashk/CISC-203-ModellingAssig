
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

from datalayer import Term
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
class StudentEnrolledCourse(Hashable): #A student enrolled in a specific course 
    """
    Represents a student's enrollment in a specific course.

    Attributes:
    - student: A Student object representing the enrolled student.
    - course: The parent object (typically a Course) of the enrolled section.

    Methods:
    - __init__(self, student, course, term, section): Initializes a new StudentEnrolled instance.
    - __repr__(self): Returns a human-readable string representation of the enrollment.
    """
    def __init__(self, student, course, term, section):
        self.student = student #a datalayer Student object
        self.course = course #a datalayer Course object

    def __repr__(self):
        return f"({str(self.student.name)} -> {str(self.course.id)})"

@proposition(E)
class StudentEnrolledCourseTerm(Hashable): #A student enrolled in a specific course of a specific term
    """
    Represents a student's enrollment in a specific course in a given term of a given year.

    Attributes:
    - student: A Student object representing the enrolled student.
    - course: The parent object (typically a Course) of the enrolled section.
    - term: The term in which the student is enrolled.

    Methods:
    - __init__(self, student, course, term, section): Initializes a new StudentEnrolled instance.
    - __repr__(self): Returns a human-readable string representation of the enrollment.
    """
    def __init__(self, student, course, term):
        self.student = student #a datalayer Student object
        self.course = course #a datalayer Course object
        self.term = term #a datalayer Term Enum

    def __repr__(self):
        return f"({str(self.student.name)} -> {str(self.course.id)} Term: {str(self.term)})"

@proposition(E)
class StudentEnrolledCourseSection(Hashable): #A student enrolled in a specific course of a specific term in a specific section
    """
    Represents a student's enrollment in a specific course section for a given term of a given year.

    Attributes:
    - student: A Student object representing the enrolled student.
    - course: The parent object (typically a Course) of the enrolled section.
    - term: The term in which the student is enrolled.
    - section: The specific course section in which the student is enrolled.

    Methods:
    - __init__(self, student, course, term, section): Initializes a new StudentEnrolled instance.
    - __repr__(self): Returns a human-readable string representation of the enrollment.
    """
    def __init__(self, student, course, term, section):
        self.student = student #a datalayer Student object
        self.course = course #a datalayer Course object
        self.term = term #a datalayer Term Enum
        self.section = section #a datalayer Section object

    def __repr__(self):
        return f"({str(self.student.name)} -> {str(self.course.id)} Term: {str(self.term)} Section: {str(self.section.class_number)})"

@proposition(E)
class CourseTermSectionTimeConflict(Hashable): #Models a conflict between 2 sections of 2 differnt courses in different terms
    def __init__(self, student, term, course1, section1, course2, section2):
        self.student = student #a datalayer Student object
        self.term = term #a datalayer Term Enum
        
        self.course1 = course1 #a datalayer Course object
        self.course2 = course2 #a datalayer Course object
        
        self.section1 = section1 #a datalayer Section object
        self.section2 = section2 #a datalayer Section object

    def __repr__(self):
        return f"( {str(self.student.name)} -> CONFLICT[{self.course1.id}-{str(self.section1.class_number)}, {self.course2.id}-{str(self.section2.class_number)}] in Term: {str(self.term)})"
    

def build_propositions(objects):
    """
    NOT USED YET
    """
    students = objects["students"]
        
    


def build_theory(objects):
    """
    #TODO
    """
    #build_propositions(objects)
    students = objects["students"]
    
    #CONSTRAINT 1
    #For every student and course, they can be enrolled in the course during only one term ex: one of "Fall", "Winter", "Summer" depending on a courses offering
    for student in students:
        for course in student.course_wish_list:
            
            ENROLLED_COURSE_TERM = []
            
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                ENROLLED_COURSE_TERM.append(StudentEnrolledCourseTerm(student, course, term))
                
            constraint.add_exactly_one(E, ENROLLED_COURSE_TERM)

    #CONSTRAINT 2
    #For every student and course, they can be enrolled in exactly one section of a course
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
                ENROLLED_COURSE_SECTIONS = [] #a list of all sections during a term for a particular course
                
                for section in term_offerings: #get the Section objects from the term_offering
                    ENROLLED_COURSE_SECTIONS.append(StudentEnrolledCourseSection(student, course, term, section))
                    
                constraint.add_at_most_one(E, ENROLLED_COURSE_SECTIONS)

    #CONSTRAINT 3
    #For every student and course, if they are not taking the course during a term they should not be enrolled in any of its sections
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                for section in term_offerings: #get the Section objects from the term_offering

                    E.add_constraint(~StudentEnrolledCourseTerm(student, course, term) >> ~StudentEnrolledCourseSection(student, course, term, section))
                
    #CONSTRAINT 4
    #For every student and every course if any sections of a course have a time conflict, both of the sections cannot be taken.
    for student in students:
        for course1 in student.course_wish_list:
            for course2 in student.course_wish_list:
                if course1 != course2: #check to ensure that the courses are different
                    offered_terms_course1 = course1.sections.get_term_offerings()
                    offered_terms_course2 = course1.sections.get_term_offerings()
                    for term1 in offered_terms_course1: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering of course1
                        for term2 in offered_terms_course2: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering of course2
                            if term1 == term2: #ensure that the terms are not different
                                term_offerings_course1 = course1.sections.get_term_collection(term1)#get course term offerings for course1
                                term_offerings_course2 = course2.sections.get_term_collection(term2)#get course term offerings for course2
                                for section_course1 in term_offerings_course1: #get the Section objects from the term offering for course 1
                                    for section_course2 in term_offerings_course2: #get the Section objects from the term offering for course 2
                                        if section_course1.has_conflict(section_course2):
                                            time_conflict_instance = CourseTermSectionTimeConflict(student, term1, course1, section_course1, course2, section_course2)
                                            constraint.add_exactly_one(E,[time_conflict_instance]) #force the premise to true #TODO I don't think this is how your suppose to do this LOL
                                            E.add_constraint(time_conflict_instance >> ~(StudentEnrolledCourseSection(student, course1, term1, section_course1) & StudentEnrolledCourseSection(student, course2, term2, section_course2)))
    
    return E
                

def display_solution(sol):
    import pprint
    pprint.pprint(sol)
    #display_assignment(sol)
    #display_student_prefs(sol)


if __name__ == "__main__":
    objects = main.create_data_layer()
    
    T = build_theory(objects)
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution:")
    sol = T.solve()

    display_solution(sol)
