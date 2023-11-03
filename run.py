
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

from datalayer import Term
import datalayer
import main #TODO needs to be removed and code needs to be added to build_theorey
import booleanlogic

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
    def __init__(self, student, course):
        self.student = student #a datalayer Student object
        self.course = course #a datalayer Course object

    def __repr__(self):
        if isinstance(self.student, datalayer.Student):
            return f"({str(self.student.name)} -> {str(self.course.id)})"
        else:
            return f"({str(self.student)} -> {str(self.course)})"

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

@proposition(E)
class CourseExclusionRequirement(Hashable):#Models if a exclusion requirement for a student's specific course is satisfied
    """
    Represents a student's course exclusion requirement.

    Attributes:
    - student: A Student object or string representing the enrolled student.
    - course: The Course object or string representing the course object.

    Methods:
    - __init__(self, student, course): Initializes a new CourseExclusionRequirement instance.
    - __repr__(self): Returns a human-readable string representation of the exclusion requirement.
    """
    def __init__(self, student, course):
        self.student = student #a datalayer Student object or string
        self.course = course #a datalayer Course object or string

    def __repr__(self):
        if isinstance(self.student, datalayer.Student): #allows for datalayer objects or strings to be passed on initialization, important for the dynamic rule evaluation
            return f"({str(self.student.name)}: {str(self.course.id)} has met the exclusion requirement)"
        else:
            return f"({str(self.student)}: {str(self.course)} has met the exclusion requirement)"

@proposition(E)
class CheckCourseExclusionsExists(Hashable): #Models an exclusion requirement for a student's specific course 
    def __init__(self, student, course, excluded_course):
        self.student = student #string
        self.course = course #a string
        self.excluded_course = excluded_course #a string

    def __repr__(self):
        if isinstance(self.student, datalayer.Student): #allows for datalayer objects or strings to be passed on initialization, important for the dynamic rule evaluation
            return f"({self.student.name}: {self.excluded_course.id} is an exclusion for {self.course.id} and is exisits"
        else:
            return f"({self.student}: {self.excluded_course} is an exclusion for {self.course} and the course exisits"

@proposition(E)
class CoursePrerequisiteRequirement(Hashable): #Models if a prerequisite requirement for a student's specific course is satisfied
    """
    Represents a student's course prerequisite requirement.

    Attributes:
    - student: A Student object or string representing the enrolled student.
    - course: The Course object or string representing the course object.

    Methods:
    - __init__(self, student, course): Initializes a new CoursePrerequisiteRequirement instance.
    - __repr__(self): Returns a human-readable string representation of the prerequisite requirement.
    """
    def __init__(self, student, course):
        self.student = student #a datalayer Student object or string
        self.course = course #a datalayer Course object or string

    def __repr__(self):
        if isinstance(self.student, datalayer.Student): #allows for datalayer objects or strings to be passed on initialization, important for the dynamic rule evaluation
            return f"({str(self.student.name)}: {str(self.course.id)} has met the prerequisite requirement)"
        else:
            return f"({str(self.student)}: {str(self.course)} has met the prerequisite requirement)"

@proposition(E)
class CheckCoursePrerequisitesExists(Hashable): #Models an prerequisite requirement for a student's specific course 
    def __init__(self, student, course, required_course):
        self.student = student #string
        self.course = course #a string
        self.required_course = required_course #a string

    def __repr__(self):
        if isinstance(self.student, datalayer.Student): #allows for datalayer objects or strings to be passed on initialization, important for the dynamic rule evaluation
            return f"({self.student.name}: {self.required_course.id} is a prerequisite for {self.course.id} and is satisfied"
        else:
           return f"({self.student}: {self.required_course} is a prerequisite for {self.course} and is satisfied"

@proposition(E)
class CourseCorequisiteRequirement(Hashable): #Models if a corequisite requirement for a student's specific course is satisfied
    """
    Represents a student's course corequisite requirement.

    Attributes:
    - student: A Student object or string representing the enrolled student.
    - course: The Course object or string representing the course object.

    Methods:
    - __init__(self, student, course): Initializes a new CoursePrerequisiteRequirement instance.
    - __repr__(self): Returns a human-readable string representation of the corequisite requirement.
    """
    def __init__(self, student, course):
        self.student = student #a datalayer Student object or string
        self.course = course #a datalayer Course object or string

    def __repr__(self):
        if isinstance(self.student, datalayer.Student): #allows for datalayer objects or strings to be passed on initialization, important for the dynamic rule evaluation
            return f"({str(self.student.name)}: {str(self.course.id)} has met the corequisite requirement)"
        else:
            return f"({str(self.student)}: {str(self.course)} has met the corequisite requirement)"

@proposition(E)
class CheckCourseCorequisitesExists(Hashable): #Models an corequisite requirement for a student's specific course 
    def __init__(self, student, course, required_course):
        self.student = student #string
        self.course = course #a string
        self.required_course = required_course #a string

    def __repr__(self):
        if isinstance(self.student, datalayer.Student): #allows for datalayer objects or strings to be passed on initialization, important for the dynamic rule evaluation
            return f"({self.student.name}: {self.required_course.id} is a corequisite for {self.course.id} and is satisfied"
        else:
           return f"({self.student}: {self.required_course} is a corequisite for {self.course} and is satisfied"



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
    
    #CONSTRAINT 0 - Course -> Term
    #For every student and course, if a student is taking a course they must be taking the course in one of the terms.
    for student in students:
        for course in student.course_wish_list:

                E.add_constraint(StudentEnrolledCourse(student, course) >> (StudentEnrolledCourseTerm(student, course, "FALL") | StudentEnrolledCourseTerm(student, course, "WINTER") | StudentEnrolledCourseTerm(student, course, "SUMMER")))
    
    #CONSTRAINT 1 - One Term Per Course Limit
    #For every student and course, they can be enrolled in the course during only one term ex: one of "Fall", "Winter", "Summer" depending on a courses offering.
    for student in students:
        for course in student.course_wish_list:
            
            ENROLLED_COURSE_TERM = []
            
            offered_terms = course.sections.get_term_offerings()
            for term in [datalayer.Term.FALL, datalayer.Term.WINTER, datalayer.Term.SUMMER]: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                if term in offered_terms:
                    ENROLLED_COURSE_TERM.append(StudentEnrolledCourseTerm(student, course, term))
                
                #If the course is not offered in a term you can't take it in that term.
                else: 
                    constraint.add_none_of(E, [StudentEnrolledCourseTerm(student, course, term)])
                
            constraint.add_at_most_one(E, ENROLLED_COURSE_TERM)

    #CONSTRAINT 2 - One Section Per Course Limit
    #For every student and course, they can be enrolled in exactly one section of a course.
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
                ENROLLED_COURSE_SECTIONS = [] #a list of all sections during a term for a particular course
                
                for section in term_offerings: #get the Section objects from the term_offering
                    ENROLLED_COURSE_SECTIONS.append(StudentEnrolledCourseSection(student, course, term, section))
                    
                constraint.add_at_most_one(E, ENROLLED_COURSE_SECTIONS)
    
    #CONSTRAINT 3 - NOT Course -> Not Term Not Section
    #For every student and every course in a students wishlist, if a student isn't enrolled in a course, then a student cannot be enrolled in any of a courses sections over any of the terms
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
                E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> StudentEnrolledCourse(student, course))
    
    #CONSTRAINT 4 - Not Term Course -> Not Term Course Sections
    #For every student and course, if they are enrolled in a course in a specific term they must be taking the course during that term.
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                for section in term_offerings: #get the Section objects from the term_offering

                    E.add_constraint(StudentEnrolledCourseSection(student, course, term, section) >> StudentEnrolledCourseTerm(student, course, term))
                
    #CONSTRAINT 5 - Course Section Time Conflict
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
    
    #CONSTRAINT 6 - Course Exclusions
    #For every student and every course in a students wishlist, if a course that a student wish's to take has an exclusion rule in
    # its requirements, then no course in the students course history or in the courses they wish to take should contain an excluded course.
    # If an exclusion is present then the propositon CourseExclusionExists will be true
    for student in students:
        for course in student.course_wish_list:
            if isinstance(course.requirements, datalayer.CourseRequirement): #if the course object has a datalayer requirement object then proceed.
                #NOTE: not all objects have datalayer requirements
                exclusion_rule = course.requirements["EXCLUSION"].criteria #get the exclusion rule
                if exclusion_rule != "NONE":
                    excluded_courses = booleanlogic.extract_courses(exclusion_rule) #get all the courses in the exclusion rule
                    
                    for check_course in excluded_courses: #loop over all courses in the exclusion rule
                        
                        exclusion_exists = CheckCourseExclusionsExists(student.name, course.id, check_course) #create a course exclusion propositon
                        
                        #If a course that is in the exclusion rule has been taken, or a student wishes to take the course then the exclusion rule has been broken
                        if check_course in str(student.course_wish_list) + str(student.completed_courses):
                            constraint.add_exactly_one(E,[exclusion_exists]) #force the proposition to true, i.e an exclusion is present
                        else:
                            constraint.add_none_of(E,[exclusion_exists]) #force the proposition to false, i.e an exclusion is not present
                            
                        #We must now evaluate the exclusion rule. This is complicated because the exculusion rule is a dynamic logical expression.
                        #Therefore we must use the exec function to dynamically create constraints.
                        #Given the exclusion rule we will map the operators "AND", "OR", "NOT" to the corresponding bauhaus operators "&", "|", "~".
                        #We will then map each course code to the propositions that were created in above step "CheckCourseExclusionsExists()".
                        #We will then build a bauhaus constraint as a string.
                        #The constraint is that the exclusion rule implies if the CourseExclusionRequirement is satisfied or not.
                        #Example "E.add_constraint((CheckCourseExclusionsExists('Student', 'Course', 'ExcludedCourse1') | CheckCourseExclusionsExists('Student', 'Course', 'ExcludedCourse1') >> ~(CourseExclusionRequirement('Student', 'Course')))"
                        #The string constraint that has been formed will then be executed using exec()
                        
                        exclusion_rule = exclusion_rule.replace(check_course, f"CheckCourseExclusionsExists('{student.name}', '{course.id}', '{check_course}')" )
                        exclusion_rule = exclusion_rule.replace("AND","&").replace("OR","|").replace("NOT", "~")
                        
                    exclusion_rule = f"(~({exclusion_rule}))"
                    requirement_met = f"(CourseExclusionRequirement('{student.name}', '{course.id}'))"
                    
                    #Equivalence Relationship #BUG OR NOT WORKING
                    #new_constraint = f"E.add_constraint(({exclusion_rule} >> {requirement_met}) & ({requirement_met} >> {exclusion_rule}))"
                    new_constraint = f"E.add_constraint(({exclusion_rule} & {requirement_met}) | (~{requirement_met} & ~{exclusion_rule}))"
                    
                    exec(new_constraint)
                else:
                    constraint.add_exactly_one(E,[CourseExclusionRequirement(student, course)]) #Force True
            
            else:
                constraint.add_exactly_one(E,[CourseExclusionRequirement(student, course)]) #Force True

    #CONSTRAINT 7 - Course Prerequisites                   
    #For every student and every course in a students wishlist, if a course that a student wish's to take has a prerequisite rule in
    # its requirements, then a prerequisite course must be in the students course history.
    for student in students:
        for course in student.course_wish_list:
            if isinstance(course.requirements, datalayer.CourseRequirement): #if the course object has a datalayer requirement object then proceed.
                #NOTE: not all objects have datalayer requirements
                prerequisite_rule = course.requirements["PREREQUISITE"].criteria #get the prerequisite rule
                if prerequisite_rule != "NONE":
                    prerequisite_courses = booleanlogic.extract_courses(prerequisite_rule) #get all the courses in the prerequisite rule
                    
                    for check_course in prerequisite_courses: #loop over all courses in the prerequisite rule
                        
                        prerequisite_exists = CheckCoursePrerequisitesExists(student.name, course.id, check_course) #create a course prerequisite propositon
                        
                        #If a course that is in the prerequisite rule has not been taken, then the prerequisite rule has been broken
                        if check_course in str(student.completed_courses):
                            constraint.add_exactly_one(E,[prerequisite_exists]) #force the proposition to true, i.e an prerequisite is present
                        
                        #If a course that is in the prerequisite rule has not already been taken and is not being taken before the course in question, then the prerequisite rule has been broken,
                        #therefore if a student is planning on taking a corequisite course, they must be taken at the same time or before.
                        elif check_course in str(student.course_wish_list):
                            E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], "FALL") >> (StudentEnrolledCourseTerm(student, course, "WINTER") | StudentEnrolledCourseTerm(student, course, "SUMMER")))
                            E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], "WINTER") >> (StudentEnrolledCourseTerm(student, course, "SUMMER")))
                            E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], "SUMMER") >> (StudentEnrolledCourse(student, course)))
                            constraint.add_exactly_one(E,[prerequisite_exists]) #force the proposition to true, i.e a prerequisite is present
                        
                        else:
                            constraint.add_none_of(E,[prerequisite_exists]) #force the proposition to false, i.e an prerequisite is not present
                            
                        #We must now evaluate the prerequisite rule. This is complicated because the prerequisite rule is a dynamic logical expression.
                        #Therefore we must use the exec function to dynamically create constraints.
                        #Given the prerequisite rule we will map the operators "AND", "OR", "NOT" to the corresponding bauhaus operators "&", "|", "~".
                        #We will then map each course code to the propositions that were created in above step "CheckCoursePrerequisitesExists()".
                        #We will then build a bauhaus constraint as a string.
                        #The constraint is that the prerequisite rule implies if the CoursePrerequisiteRequirement is satisfied or not.
                        #Example "E.add_constraint(~(CheckCoursePrerequisitesExists('Student', 'Course', 'PrerequisiteCourse1') | CheckCoursePrerequisitesExists('Student', 'Course', 'PrerequisiteCourse1') >> ~(CoursePrerequisiteRequirement('Student', 'Course')))"
                        #The string constraint that has been formed will then be executed using exec()
                        
                        prerequisite_rule = prerequisite_rule.replace(check_course, f"CheckCoursePrerequisitesExists('{student.name}', '{course.id}', '{check_course}')" )
                        prerequisite_rule = prerequisite_rule.replace("AND","&").replace("OR","|").replace("NOT", "~")
                        prerequisite_rule = f"({prerequisite_rule})"
                        requirement_met = f"(CoursePrerequisiteRequirement('{student.name}', '{course.id}'))"
                    
                    #Equivalence Relationship
                    new_constraint = f"E.add_constraint(({prerequisite_rule} & {requirement_met}) | (~{requirement_met} & ~{prerequisite_rule}))"
                    exec(new_constraint)

                else:
                    constraint.add_exactly_one(E,[CoursePrerequisiteRequirement(student, course)]) #Force True
            
            else:
                constraint.add_exactly_one(E,[CoursePrerequisiteRequirement(student, course)]) #Force True

    #CONSTRAINT 8 - Course Corequisites
    #For every student and every course in a students wishlist, if a course that a student wish's to take has a corequisite rule in
    # its requirements, then a coerequisite course must be in the students course history.
    for student in students:
        for course in student.course_wish_list:
            if isinstance(course.requirements, datalayer.CourseRequirement): #if the course object has a datalayer requirement object then proceed.
                #NOTE: not all objects have datalayer requirements
                corequisite_rule = course.requirements["COREQUISITE"].criteria #get the corequisite rule
                
                if corequisite_rule != "NONE":
                    corequisite_courses = booleanlogic.extract_courses(corequisite_rule) #get all the courses in the corequisite rule
                    
                    for check_course in corequisite_courses: #loop over all courses in the corequisite rule
                        
                        corequisite_exists = CheckCourseCorequisitesExists(student.name, course.id, check_course) #create a course corequisite propositon
                        
                        #If a course that is in the corequisite rule has not already been taken, then the corequisite rule has been broken
                        if check_course in str(student.completed_courses):
                            constraint.add_exactly_one(E,[corequisite_exists]) #force the proposition to true, i.e a corequisite is present
                        
                        #If a course that is in the corequisite rule has not already been taken and is not being taken at the same time as the course in question or before,
                        # then the corequisite rule has been broken,
                        #therefore if a student is planning on taking a corequisite course, they must be taken at the same time or before.
                        elif check_course in str(student.course_wish_list):
                            E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], "FALL") >> (StudentEnrolledCourseTerm(student, course, "FALL") | StudentEnrolledCourseTerm(student, course, "WINTER") | StudentEnrolledCourseTerm(student, course, "SUMMER")))
                            E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], "WINTER") >> (StudentEnrolledCourseTerm(student, course, "WINTER") | StudentEnrolledCourseTerm(student, course, "SUMMER")))
                            E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], "SUMMER") >> (StudentEnrolledCourseTerm(student, course, "SUMMER")))
                            constraint.add_exactly_one(E,[corequisite_exists]) #force the proposition to true, i.e a corequisite is present
                        else:
                            constraint.add_none_of(E,[corequisite_exists]) #force the proposition to false, i.e a corequisite is not present
                            
                        #We must now evaluate the corequisite rule. This is complicated because the corequisite rule is a dynamic logical expression.
                        #Therefore we must use the exec function to dynamically create constraints.
                        #Given the corequisite rule we will map the operators "AND", "OR", "NOT" to the corresponding bauhaus operators "&", "|", "~".
                        #We will then map each course code to the propositions that were created in above step "CheckCoursePrerequisitesExists()".
                        #We will then build a bauhaus constraint as a string.
                        #The constraint is that the corequisite rule implies if the CourseCorequisiteRequirement is satisfied or not.
                        #Example "E.add_constraint(~(CheckCourseCorequisitesExists('Student', 'Course', 'CorequisiteCourse1') | CheckCourseCorequisitesExists('Student', 'Course', 'CorequisiteCourse1') >> ~(CourseCorequisiteRequirement('Student', 'Course')))"
                        #The string constraint that has been formed will then be executed using exec()
                        
                        corequisite_rule = corequisite_rule.replace(check_course, f"CheckCourseCorequisitesExists('{student.name}', '{course.id}', '{check_course}')" )
                        corequisite_rule = corequisite_rule.replace("AND","&").replace("OR","|").replace("NOT", "~")
                        corequisite_rule = f"({corequisite_rule})"
                        requirement_met = f"(CourseCorequisiteRequirement('{student.name}', '{course.id}'))"
                    
                    #Equivalence Relationship
                    new_constraint = f"E.add_constraint(({corequisite_rule} & {requirement_met}) | (~{requirement_met} & ~{corequisite_rule}))"
                    exec(new_constraint)
                else:
                    constraint.add_exactly_one(E,[CourseCorequisiteRequirement(student, course)]) #Force True
            
            else:
                constraint.add_exactly_one(E,[CourseCorequisiteRequirement(student, course)]) #Force True
                
    #CONSTRAINT 9 - Course -> Requirements Are Met
    #For every student and every course in a students wishlist, if a courses exclusions, prerequisites, corequisistes and program requirements
    # are all satisfied then the student can enroll in the course.
    for student in students:
        for course in student.course_wish_list:
            E.add_constraint(StudentEnrolledCourse(student, course) >> (CourseExclusionRequirement(student, course) & CoursePrerequisiteRequirement(student, course) & CourseCorequisiteRequirement(student, course)))

    #CONSTRAINT 10 - A student can take at most 10 courses, and wishes to take the most possible courses up to 10
    for student in students:
        all_courses = []
        for course in student.course_wish_list:
            all_courses.append(StudentEnrolledCourse(student, course))
            #constraint.add_exactly_one(E, StudentEnrolledCourse(student, course)) #forces all 'wished' courses to be taken (if there is a conflict there will be no solutions)

        # k = len(all_courses)
        # if k > 10:
        #     k = 10
        # constraint.add_at_most_k(E, k, all_courses)
    
    return E
                

def display_solution(sol):
    import pprint
    pprint.pprint(sol)
    #display_assignment(sol)
    #display_student_prefs(sol)

def display_course_selection(sol, objects):
    students = objects["students"]
    for student in students:
        course_collection = {datalayer.Term.FALL: [], datalayer.Term.WINTER: [], datalayer.Term.SUMMER: []}
        for course in student.course_wish_list:
            if sol[StudentEnrolledCourse(student, course)]:
                
                offered_terms = course.sections.get_term_offerings()
                for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                    if sol[StudentEnrolledCourseTerm(student, course, term)]:
                        
                        term_offerings = course.sections.get_term_collection(term)#get course term offerings
                        for section in term_offerings: #get the Section objects from the term_offering
                            if sol[StudentEnrolledCourseSection(student, course, term, section)]:
                                course_collection[term].append(f"{section.courseid}-{section.class_number}")
                                
        print(f"{student.name}: Has been enrolled in Fall:{course_collection[datalayer.Term.FALL]}, Winter:{course_collection[datalayer.Term.WINTER]}, Summer:{course_collection[datalayer.Term.SUMMER]}")

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

    if count_solutions(T) != 0:
        print("\n\n\n\n")
        display_course_selection(sol, objects)
        print("\n\n")
        
