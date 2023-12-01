
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from bauhaus import Encoding, proposition, constraint, Or, And

import datalayer
import utils

"""
    Builds, Creates and Compiles the course scheduling solver, also defines propostions and constraints for modeling course
    scheduling and enrolment considering various enrolment requirements and time conflicts.
"""

from nnf import config
config.sat_backend = "kissat"

E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

#PROPOSITIONS
#region
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
        return f"({str(self.student.name)} -> CONFLICT [{self.course1.id}-{str(self.section1.class_number)}, {self.course2.id}-{str(self.section2.class_number)}] in Term: {str(self.term)})"

@proposition(E)
class CourseTermSectionAvailableCapacity(Hashable): #Models a classes availability, depending on capacity
    def __init__(self, course, term, section):
        self.term = term #a datalayer Term Enum
        self.course = course #a datalayer Course object
        self.section = section #a datalayer Section object

    def __repr__(self):
        return f"({str(self.course.id)} Term: {str(self.term)} Section: {str(self.section.class_number)} has capacity:)"

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

@proposition(E)
class StudentCourseRequiredTerm(Hashable): #Models the fact that a student may be required to take a specific course during a specific term to satisfy prerequisites
    def __init__(self, student, course, term):
        self.student = student #a datalayer Student object
        self.course = course #a datalayer Course object
        self.term = term #a datalayer Term Enum

    def __repr__(self):
        return f"({self.student}: {self.course} must be taken in {self.term}"

@proposition(E)
class Friendship(Hashable): #Models a friendship among student
    def __init__(self, student1, student2):
        self.student1 = student1 #a datalayer Student object
        self.student2 = student2 #a datalayer Student object

    def __repr__(self):
        return f"({self.student1.name} + {self.student2.name})"
#endregion


def build_propositions(objects):
    """
    NOT USED YET
    """
    students = objects["students"]

    
#CONSTRAINTS
def enrolment_rules(objects):
    """
    Enrolment Rules for Student Course Enrolment

    Defines constraints related to student course enrolment.
    Covers rules such as course-term limits and section limts.

    Args:
        objects (dict): A dictionary containing datalayer collections.

    Returns:
        None
    """
    
    students = objects["students"]
    
    #CONSTRAINT 0 - Course -> Term
    #For every student and course, if a student is taking a course they must be taking the course in one of the terms.
    for student in students:
        if len(student.course_wish_list) != 0:
            for course in student.course_wish_list:
                offered_terms = course.sections.get_term_offerings()
                offerings = []
                
                for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                    offerings.append(StudentEnrolledCourseTerm(student, course, term))
                    
                offerings = Or(offerings)  
                E.add_constraint(StudentEnrolledCourse(student, course) >> (offerings))
        else:
            utils.warn(f"{student} does not wish to take any courses is this an error?")
        
    #CONSTRAINT 0.1 - One Term Per Course
    #For every student and course, they can be enrolled in the course during only one term ex: one of "Fall", "Winter", "Summer" depending on a courses offering.
    for student in students:
        for course in student.course_wish_list:
            
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                other_terms = []
                for other_term in offered_terms:
                    if term != other_term:
                        other_terms.append(StudentEnrolledCourseTerm(student, course, other_term))

                other_terms = Or(other_terms)
                E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> (~other_terms))

    
    #CONSTRAINT 1 - Term -> Section
    #For every student and course, they can be enrolled in exactly one section of a course.
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
                ENROLLED_COURSE_SECTIONS = [] #a list of all sections during a term for a particular course
                
                for section in term_offerings: #get the Section objects from the term_offering
                    ENROLLED_COURSE_SECTIONS.append(StudentEnrolledCourseSection(student, course, term, section))
                    
                ENROLLED_COURSE_SECTIONS_OPTIONS = Or(ENROLLED_COURSE_SECTIONS)
                E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> ENROLLED_COURSE_SECTIONS_OPTIONS) #BUG
                #constraint.add_at_most_one(E, ENROLLED_COURSE_SECTIONS) #BUG
    
    #CONSTRAINT 1.1 - One Section per Course 
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
                
                for section in term_offerings: #get the Section objects from the term_offering
                    all_other_sections = []
                    for other_section in term_offerings: #get the Section objects from the term_offering
                        if section != other_section:
                            all_other_sections.append(StudentEnrolledCourseSection(student, course, term, other_section))
                    
                    all_other_sections = Or(all_other_sections)
                    E.add_constraint(StudentEnrolledCourseSection(student, course, term, section) >> ~all_other_sections)
    
    #CONSTRAINT 1.2 - Not Term Course -> Not Term Course Sections
    #For every student and course, if they are enrolled in a course in a specific term they must be taking the course during that term.
    for student in students:
        for course in student.course_wish_list:
            offered_terms = course.sections.get_term_offerings()
            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                term_offerings = course.sections.get_term_collection(term)#get course term offerings
                for section in term_offerings: #get the Section objects from the term_offering

                    E.add_constraint(StudentEnrolledCourseSection(student, course, term, section) >> StudentEnrolledCourseTerm(student, course, term))

    #CONSTRAINT 10 - A student can take at most 10 courses, and wishes to take the most possible courses up to 10
    for student in students:
        all_courses = []
        for course in student.course_wish_list:
            all_courses.append(StudentEnrolledCourse(student, course))
            constraint.add_exactly_one(E, StudentEnrolledCourse(student, course)) #forces all 'wished' courses to be taken (if there is a conflict there will be no solutions)

        # k = len(all_courses)
        # if k > 10:
        #     k = 10
        # constraint.add_at_most_k(E, k, all_courses)
    
def enrolment_restrictions(objects):
    """
    Enrolment Restrictions for Student Course Enrolment

    Defines constraints related to enrolment restrictions, such as course section time conflicts and enrolment capacity limits.

    Args:
        objects (dict): A dictionary containing datalayer collections.

    Returns:
        None
    """
    
    students = objects["students"]
    
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

    #CONSTRAINT 6 - Section Enrolment Capacity
    #A Student can only enroll in a section if there is capacity
    for student in students:
        for course in student.course_wish_list:
            offered_terms_course = course.sections.get_term_offerings()
            for term in offered_terms_course: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering of course
                term_offerings_course = course.sections.get_term_collection(term)#get course term offerings for course
                for section_course in term_offerings_course: #get the Section objects from the term offering for course
                    
                    has_capacity = CourseTermSectionAvailableCapacity(course, term, section_course)
                    
                    if section_course.enrollment_total < section_course.enrollment_capacity: #if a section has capacity for a student enrolment set it to true
                        constraint.add_exactly_one(E,[has_capacity])
                    else:
                        constraint.add_none_of(E,[has_capacity]) #otherwise false
                        
                    E.add_constraint(StudentEnrolledCourseSection(student, course, term, section_course) >> CourseTermSectionAvailableCapacity(course, term, section_course)) #if a student is enrolled in a section, there must be capacity.


    #CONSTRAINT 7 -Enroll only as many Students in a Section as there is room
    sections = {}
    for student in students:
        for course in student.course_wish_list:
            offered_terms_course = course.sections.get_term_offerings()
            for term in offered_terms_course: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering of course
                term_offerings_course = course.sections.get_term_collection(term)#get course term offerings for course
                for section_course in term_offerings_course: #get the Section objects from the term offering for course
                    
                    #create a dictionary of all students who might wish to enroll in a course
                    if section_course in sections:
                        sections[section_course.id].append(StudentEnrolledCourseSection(student, course, term, section_course))
                    else:
                        sections[section_course.id] = [StudentEnrolledCourseSection(student, course, term, section_course)]
    
    for id, possible_students in sections.items():
        allowed_enrolment = datalayer.Sections.ALLSECTIONS[id].enrollment_capacity - datalayer.Sections.ALLSECTIONS[id].enrollment_total
        number_wish_enrolled = len(possible_students)
        
        if allowed_enrolment == 0: #no room for enrolment, dont enroll anyone
            constraint.add_none_of(E, [possible_students])
        
        elif number_wish_enrolled > allowed_enrolment: #enroll only x amount of students, where x is the number of students till ocupancy is full
            constraint.add_at_most_k(E, allowed_enrolment, [possible_students])
        
def enrolment_requirements(objects):
    """
    Enrolment Requirements for Student Course Enrolment

    Defines constraints related to course prerequisites, exclusions, and corequisites.
    Ensures that students meet necessary requirements before enrolling in courses.

    Args:
        objects (dict): A dictionary containing datalayer collections.

    Returns:
        None
    """
    students = objects["students"]
    
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
                    excluded_courses = utils.extract_courses(exclusion_rule) #get all the courses in the exclusion rule
                    
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

    #CONSTRAINT 7 - Course Prerequisites     #BUG              
    #For every student and every course in a students wishlist, if a course that a student wish's to take has a prerequisite rule in
    # its requirements, then a prerequisite course must be in the students course history.
    for student in students:
        for course in student.course_wish_list:
            if isinstance(course.requirements, datalayer.CourseRequirement): #if the course object has a datalayer requirement object then proceed.
                #NOTE: not all objects have datalayer requirements
                prerequisite_rule = course.requirements["PREREQUISITE"].criteria #get the prerequisite rule
                if prerequisite_rule != "NONE":
                    prerequisite_courses = utils.extract_courses(prerequisite_rule) #get all the courses in the prerequisite rule
                    
                    for check_course in prerequisite_courses: #loop over all courses in the prerequisite rule
                        
                        prerequisite_exists = CheckCoursePrerequisitesExists(student.name, course.id, check_course) #create a course prerequisite propositon
                        
                        #If a course that is in the prerequisite rule has not been taken, then the prerequisite rule has been broken
                        if check_course in str(student.completed_courses):
                            constraint.add_exactly_one(E,[prerequisite_exists]) #force the proposition to true, i.e an prerequisite is present
                        
                        #If a course that is in the prerequisite rule has not already been taken and is not being taken before the course in question, then the prerequisite rule has been broken,
                        #therefore if a student is planning on taking a corequisite course, they must be taken at the same time or before.
                        elif check_course in str(student.course_wish_list):
                            offered_terms = course.sections.get_term_offerings()
                            for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                                other_terms = []
                                
                                if term == datalayer.Term.FALL:
                                    if datalayer.Term.WINTER in offered_terms:
                                        other_terms.append(datalayer.Term.WINTER)
                                    if datalayer.Term.SUMMER in offered_terms:
                                        other_terms.append(datalayer.Term.SUMMER)
                                    
                                elif term == datalayer.Term.WINTER and datalayer.Term.SUMMER in offered_terms and datalayer.Term.SUMMER:
                                    other_terms.append(datalayer.Term.SUMMER)

                                        
                                if other_terms != []:
                                    options = []
                                    for o_term in other_terms:
                                        options.append(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], o_term))
                                    options = Or(options)
                                    
                                    E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> (options))
                                    
                                    
                                else:
                                    E.add_constraint(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], term) >> ~(StudentEnrolledCourse(student, course))) #BUG
                                    
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

    #CONSTRAINT 8 - Course Corequisites #BUG
    #For every student and every course in a students wishlist, if a course that a student wish's to take has a corequisite rule in
    # its requirements, then a coerequisite course must be in the students course history.
    for student in students:
        for course in student.course_wish_list:
            if isinstance(course.requirements, datalayer.CourseRequirement): #if the course object has a datalayer requirement object then proceed.
                #NOTE: not all objects have datalayer requirements
                corequisite_rule = course.requirements["COREQUISITE"].criteria #get the corequisite rule
                
                if corequisite_rule != "NONE":
                    corequisite_courses = utils.extract_courses(corequisite_rule) #get all the courses in the corequisite rule
                    
                    for check_course in corequisite_courses: #loop over all courses in the corequisite rule
                        
                        corequisite_exists = CheckCourseCorequisitesExists(student.name, course.id, check_course) #create a course corequisite propositon
                        
                        #If a course that is in the corequisite rule has not already been taken, then the corequisite rule has been broken
                        if check_course in str(student.completed_courses):
                            constraint.add_exactly_one(E,[corequisite_exists]) #force the proposition to true, i.e a corequisite is present
                        
                        #If a course that is in the corequisite rule has not already been taken and is not being taken at the same time as the course in question or before,
                        # then the corequisite rule has been broken,
                        #therefore if a student is planning on taking a corequisite course, they must be taken at the same time or before.
                        
                        elif check_course in str(student.course_wish_list):
                            offered_terms = course.sections.get_term_offerings()
                            for term in  offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                                other_terms = []
                                if term == datalayer.Term.SUMMER:
                                    if datalayer.Term.FALL in offered_terms:
                                        other_terms.append(datalayer.Term.FALL)
                                    if datalayer.Term.WINTER in offered_terms:
                                        other_terms.append(datalayer.Term.WINTER)
                                    other_terms.append(datalayer.Term.SUMMER)
                                        
                                elif term == datalayer.Term.WINTER:
                                    if datalayer.Term.FALL in offered_terms:
                                        other_terms.append(datalayer.Term.FALL)
                                    other_terms.append(datalayer.Term.WINTER)
                                    
                                elif term == datalayer.Term.FALL:
                                    other_terms.append(datalayer.Term.FALL)
                                
                                options = []
                                for o_term in other_terms:
                                    options.append(StudentEnrolledCourseTerm(student, student.course_wish_list[check_course], o_term))
                                options = Or(options)
                                
                                E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> (options))
                                
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

def friendship(objects):
    """
    Friendship Constraints

    Defines constraints related to friendships between students.
    Ensures that if students are friends, certain conditions are met for enrolment in the same course.

    Args:
        objects (dict): A dictionary containing datalayer collections.

    Returns:
        None
    """
    
    students = objects["students"]
    
    #CONSTRAINT 11 - If students are friends, then they must have a friendship
    for student1 in students:
        for student2 in students:
            if student1 != student2:
                if student1 in student2.friends and student2 in student1.friends:
                    constraint.add_exactly_one(E, Friendship(student1, student2))

                else:
                    constraint.add_none_of(E, Friendship(student1, student2))
                
    #CONSTRAINT 12 - If students are friends and wish to be enrolled in the same course, they may. If and only if there are no prior restrictions that affect them both.
    for student in students:
        if student.has_friends():
            for friend in student.friends:
                for course in friend.shared_courses:
                    if student.is_reciprocal(friend, course): #if the friendship and course selection is mutual
                        friend = datalayer.Students.ALLSTUDENTS[friend.name]
                        
                        term_options = [] #the term options 2 students can take a course in
                        section_options = [] #the section options 2 students can take a course in
                        for term in datalayer.Term:
                            term_offerings_course = course.sections.get_term_collection(term)
                            term_options.append(StudentEnrolledCourseTerm(student, course, term) & StudentEnrolledCourseTerm(friend, course, term))
                            
                            for section in term_offerings_course:
                                section_options.append(StudentEnrolledCourseSection(student, course, term, section) & StudentEnrolledCourseSection(friend, course, term, section))
                        
                        common_term = Or(term_options)
                        common_section = Or(section_options)
                        
                            
                        E.add_constraint((StudentEnrolledCourse(student, course) & StudentEnrolledCourse(friend, course) & Friendship(student1, student2)) >> (common_section))
    
        #TODO
    

#BUILDER
def build_theory(objects):
    """
    Creates the theory by executing sub-functions for enrolment rules, restrictions, requirements, and friendship constraints.

    Args:
        objects (dict): A dictionary of datalayer collections.
    Returns:
        BauhausTheory: A compiled bauhaus theory.
    """
    enrolment_rules(objects)
    enrolment_restrictions(objects)
    enrolment_requirements(objects)
    friendship(objects)
                      
    return E

#EXECUTER               
def execute(objects):
    """
    Creates and attempts to compile the theory. If successful, returns the theory and its solution.

    Args:
        objects (dict): A dictionary of datalayer collections.
        
    Returns:
        dict: A dictionary containing the compiled bauhaus theory and its solution.
    """
    
    T = build_theory(objects)
    
    # Don't compile until you're finished adding all your constraints!
    try:
        # Your code that may raise the ValueError
        T = T.compile()
    except ValueError as ve:
        if len(objects["students"]) == 1 and len(next(iter(objects["students"])).course_wish_list) == 0:
            utils.warn(f"Caught a ValueError During CompileTime: Does the student wish to take any courses?")
            raise SystemExit()
        
        else:
            # Handling the ValueError
            utils.warn(f"Caught a ValueError During CompileTime: this is most likely the result of a misconfigured data-layer")
            raise SystemExit(ve)
            # Additional error handling or cleanup code can go here
    
    except:
        utils.warn(f"Caught a ValueError During CompileTime: Does the student wish to take any courses?")
        raise SystemExit()
    
    return {"Theory": T, "Solution": T.solve()}
    
    
if __name__ == "__main__":
    pass