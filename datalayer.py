import json
from aenum import MultiValueEnum
from enum import Enum
from datetime import datetime, timedelta
from collections.abc import Mapping
import sys

"""
Object-Oriented JSON Data Modeling

Defines classes for representing Queens courses, Queens departments and Queens course sections, as well as collections for courses, departments and sections.

Module-level attributes:
- data: A module attribute containing all data initalized by the datalayer
- testid: A module attribute storing the test id to prevent json remapping. 

Classes:
- Term: An Enum representing academic terms, defines three academic terms FALL, WINTER, SUMMER.
- AcademicYear: An Enum representing academic years, defines four academic years FIRSTYEAR, SECONDYEAR, THIRDYEAR, FOURTHYEAR.

- Course: Represents a course with its attributes.
- Courses: Represents a collection of Course objects.

- CourseRequirement: Represents all enrolment requirements of a Course.
- CourseRequirementSpecific: Represents a specific requirement for a Course. ex. PREREQUISITE, COREQUISITE, EXCLUSION, COREQUISITE
- CourseRequirements: Represents a collection of CourseRequirement objects.

- Department: Represents a academic department.
- Departments: Represents a collection of Department objects.

- TermLevelSection: (Private) Represents a the parent Section of a Course during a specific Term. Contains links to the equivalent Course object.
- Section: Represents a specific course section (i.e. 001).
- SectionDate: Represents a Course Section's date (i.e. Monday 9:30am).
- SectionDates: Represents a collection of SectionDate objects.
- Sections: Represents a collection of Section objects.

- Student: Represents a specific student.
- Students: Represents a collection of Student objects.

- Friend: Represents a specific friend of a Student.
- Friends: Represents a collection of Friend objects.

Functions:
- mapDepartments: Maps data from a buildings.json file to a Departments collection.
- mapRequirements: Map data from a requirements.json file to a CourseRequirements collection.
- mapSections: Maps data from a sections.json file to a Sections collection.
- mapCourses: Maps data from a courses.json file to a Courses collection.
- mapStudents: Maps data from a students.json file to a Students collection.
- mapFriends: Maps friend data from a students.json file to a Friends collection.
"""

# Module-level
data = None
testid = 999999


#ENUM Classes
class Term(MultiValueEnum):
    """
    Enum representing academic terms.
    
    This enum defines three academic terms:
    - FALL: Representing the fall term.
    - WINTER: Representing the winter term.
    - SUMMER: Representing the summer term.
    """
    FALL = "FALL", "Fall", "fall", 1
    WINTER = "WINTER", "Winter", "winter", 2
    SUMMER = "SUMMER", "Summer", "summer", 3

    def __str__(self):
        """
        Return a string representation of the enum member.
        """
        return self.value  # Using the first value in the member's tuple
    
class AcademicYear(Enum):
    """
    Enum representing academic years.

    This enum defines four academic years:
    - FIRSTYEAR: Representing the first academic year.
    - SECONDYEAR: Representing the second academic year.
    - THIRDYEAR: Representing the third academic year.
    - FOURTHYEAR: Representing the fourth academic year.
    """
    FIRSTYEAR = "FIRSTYEAR"
    SECONDYEAR = "SECONDYEAR"
    THIRDYEAR = "THIRDYEAR"
    FOURTHYEAR = "FOURTHYEAR"

#Course Classes
class Course:
    """
    Represents a Queens course with its attributes.

    Attributes:
        id (str): The course ID.
        department (str): The department offering the course.
        course_code (str): The code of the course.
        course_name (str): The name of the course.
        sections (Sections): A Sections object.
        campus (str): The campus where the course is offered.
        description (str): A description of the course.
        grading_basis (str): The grading basis for the course.
        course_components (dict): A dictionary representing course components.
        requirements (str): Prerequisites and requirements for the course.
        add_consent (str): Additional consent information.
        drop_consent (str): Information regarding consent for dropping the course.
        academic_level (str): The academic level (e.g., Undergraduate).
        academic_group (str): The academic group to which the course belongs.
        academic_org (str): The academic organization offering the course.
        units (float): The number of course units.
        CEAB (dict): A dictionary representing CEAB (Canadian Engineering Accreditation Board) information.

    Methods:
        __str__(): Returns a string representation of the Course instance.
        is_offered_in_term(term): Returns True if the course is offered during a specific Term.
    """
    def __init__(self, id, department, course_code, course_name, campus, description, grading_basis,
                 course_components, requirements, add_consent, drop_consent, academic_level,
                 academic_group, academic_org, units, CEAB):
        """
        Initializes a Course instance.
        """
        self.id = id
        self.department = department
        self.course_code = course_code
        self.course_name = course_name
        self.sections = Sections()
        self.campus = campus
        self.description = description
        self.grading_basis = grading_basis
        self.course_components = course_components  # course_components is a dictionary
        self.requirements = requirements
        self.add_consent = add_consent
        self.drop_consent = drop_consent
        self.academic_level = academic_level
        self.academic_group = academic_group
        self.academic_org = academic_org
        self.units = units
        self.CEAB = CEAB  # CEAB is a dictionary

    @property
    def id(self):
        """
        Get the course ID.
        """
        return self._id

    @id.setter
    def id(self, new_id):
        """
        Set the ID of the course.

        Args:
            new_id (str): The new course ID.
        """
        self._id = new_id

    @property
    def department(self):
        """
        Get the department offering the course.
        """
        return self._department

    @department.setter
    def department(self, value):
        """
        Set the department of the course.

        Args:
            value (str): The department to set.

        Returns:
            None
        """
        self._department = value

    @property
    def course_code(self):
        """
        Get the code of the course.
        """
        return self._course_code

    @course_code.setter
    def course_code(self, value):
        """
        Set the course code.

        Args:
            value (str): The course code to set.

        Returns:
            None
        """
        self._course_code = value

    @property
    def course_name(self):
        """
        Get the name of the course.
        """
        return self._course_name

    @course_name.setter
    def course_name(self, value):
        """
        Set the name of the course.

        Args:
            value (str): The name to set.

        Returns:
            None
        """
        self._course_name = value

    @property
    def sections(self):
        """
        Get the dictionary of Sections objects that are connected to the Course object.
        """
        return self._sections

    @sections.setter
    def sections(self, sections):
        """
        Set the sections attribute to a dictionary of Sections objects that are connected to this Course.

        Args:
            value (Sections): The Sections to set.

        Returns:
            None
        """
        self._sections = sections
    
    @property
    def campus(self):
        """
        Get the campus where the course is offered.
        """
        return self._campus

    @campus.setter
    def campus(self, value):
        """
        Set the campus where the course is offered.

        Args:
            value (str): The campus to set.

        Returns:
            None
        """
        self._campus = value
    
    @property
    def description(self):
        """
        Get a description of the course.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the description of the course.

        Args:
            value (str): The description to set.

        Returns:
            None
        """
        self._description = value

    @property
    def grading_basis(self):
        """
        Get the grading basis for the course.
        """
        return self._grading_basis

    @grading_basis.setter
    def grading_basis(self, value):
        """
        Set the grading basis of the course.

        Args:
            value (str): The grading basis to set.

        Returns:
            None
        """
        self._grading_basis = value

    @property
    def course_components(self):
        """
        Get the course components (as a dictionary).
        """
        return self._course_components

    @course_components.setter
    def course_components(self, value):
        """
        Set the course components (as a dictionary).

        Args:
            value (dict): The course components to set.

        Returns:
            None
        """
        self._course_components = value

    @property
    def requirements(self):
        """
        Get the prerequisites and requirements for the course.
        """
        return self._requirements

    @requirements.setter
    def requirements(self, value):
        """
        Set the requirements for the course.

        Args:
            value (str): The requirements to set.

        Returns:
            None
        """
        self._requirements = value

    @property
    def add_consent(self):
        """
        Get additional consent information.
        """
        return self._add_consent

    @add_consent.setter
    def add_consent(self, value):
        """
        Set additional consent information.

        Args:
            value (str): The additional consent information to set.

        Returns:
            None
        """
        self._add_consent = value

    @property
    def drop_consent(self):
        """
        Get information regarding consent for dropping the course.
        """
        return self._drop_consent

    @drop_consent.setter
    def drop_consent(self, value):
        """
        Set drop consent information.

        Args:
            value (str): The drop consent information to set.

        Returns:
            None
        """
        self._drop_consent = value

    @property
    def academic_level(self):
        """
        Get the academic level (e.g., Undergraduate).
        """
        return self._academic_level

    @academic_level.setter
    def academic_level(self, value):
        """
        Set the academic level of the course.

        Args:
            value (str): The academic level to set.

        Returns:
            None
        """
        self._academic_level = value

    @property
    def academic_group(self):
        """
        Get the academic group to which the course belongs.
        """
        return self._academic_group

    @academic_group.setter
    def academic_group(self, value):
        """
        Set the academic group of the course.

        Args:
            value (str): The academic group to set.

        Returns:
            None
        """
        self._academic_group = value

    @property
    def academic_org(self):
        """
        Get the academic organization offering the course.
        """
        return self._academic_org
    
    @academic_org.setter
    def academic_org(self, value):
        """
        Set the academic organization of the course.

        Args:
            value (str): The academic organization to set.

        Returns:
            None
        """
        self._academic_org = value
    
    @property
    def units(self):
        """
        Get the number of course units.
        """
        return self._units

    @units.setter
    def units(self, value):
        """
        Set the number of units for the course.

        Args:
            value (float): The number of units to set.

        Returns:
            None
        """
        self._units = value

    @property
    def CEAB(self):
        """
        Get CEAB (Canadian Engineering Accreditation Board) information (as a dictionary).
        """
        return self._CEAB

    @CEAB.setter
    def CEAB(self, value):
        """
        Setter for CEAB.

        Args:
            value (dict): A dictionary representing CEAB information.
        """
        self._CEAB = value

    def __str__(self):
        """
        Returns a string representation of the course.

        Returns:
            str: A formatted string with course information.
        """
        return f"{self.id}"

    def is_offered_in_term(self, term):
        """
        Checks if the course is offered in a specific academic term.

        Args:
            term (str): The academic term to check for (e.g., "Fall 2023").

        Returns:
            bool: True if the course is offered in the specified term, False otherwise.
        """
        if not isinstance(term, Term):
            term = Term(term)
        return len(self._sections.get_term_collection(term)) > 0

class Courses(Mapping):
    ALLCOURSES = None

    """
    Represents a collection of Course objects with the ability to manage, search, and iterate through them.

    Attributes:
        courses (dict): A dictionary that stores Course objects by their unique IDs.

    Methods:
        add_course(self, course): Add a Course object to the collection.
        add_courses(self, courses): Add multiple Course objects to the collection.
        find_course_by_id(self, id): Find a Course by its unique identifier.
        __str__(self): Returns a string representation of the list of Course objects.
        __iter__(self): Make the Courses class iterable. This method returns an iterator.
        __next__(self): Get the next Course object in the iteration.
        __len__(self): Get the number of Course objects in the collection.
        __contains__(self, item): Check if a Course object is in the collection.
        __getitem__(self, item): Retrieve a Course object by its unique ID.
        add_items(self, key, value): Add a Course object to the collection using a unique identifier (ID).

    """
    def __init__(self, courses=None):
        """
        Initializes a Courses instance with an optional dictionary of Courses.

        Args:
            courses (dict, optional): A dictionary of Course objects indexed by course ID.
                Default is None, which creates an empty dictionary.
        """
        self._courses = {}  # Use a dictionary to store courses by ID
        if courses is not None:
            self.add_courses(courses)

    @property
    def courses(self):
        """
        Get the list of Courses.
        """
        return list(self._courses.values())  # Convert dictionary values to a list

    def add_course(self, course):
        """
        Add a Course to the collection.

        Args:
            course (Course): The Course object to be added.
        """
        if course is not None:
            self._courses[course.id] = course  # Use course ID as the key in the dictionary

    def add_courses(self, courses):
        """
        Add multiple courses to the collection.

        Args:
            courses (list of Course): A list of Course objects to be added.
        """
        for course in courses:
            self.add_course(course)

    def find_course_by_id(self, id):
        """
        Find a Course by its unique identifier.

        Args:
            id (str): The unique identifier of the Course to search for.

        Returns:
            Course or None: The Course object if found, or None if not found.
        """
        return self._courses.get(id, None)  # Use dictionary's get method

    def __str__(self):
        """
        Returns a string representation of the list of Course objects.

        Returns:
            str: A list with information for each Course.
        """
        return str([str(course) for course in self._courses.values()])

    def __iter__(self):
        """
        Make the Courses class iterable. This method returns an iterator.
        """
        self._current_index = 0
        self._course_list = list(self._courses.values())
        return self

    def __next__(self):
        """
        Get the next Course object in the iteration.
        """
        if self._current_index < len(self._course_list):
            course = self._course_list[self._current_index]
            self._current_index += 1
            return course
        raise StopIteration

    def __len__(self):
        """
        Get the number of Course objects in the collection.

        Returns:
            int: The number of Course objects in the collection.
        """
        return len(self._courses)

    def __contains__(self, item):
        """
        Check if a Course object is in the collection.

        Args:
            item: The Course object to check for presence in the collection.

        Returns:
            bool: True if the Course object is in the collection, False otherwise.
        """
        if isinstance(item, Course):
            return (item.id in self._courses)
        elif isinstance(item, str):
            return (item in self._courses)
        else:
            return False 

    def __getitem__(self, item):
        """
        Retrieve a Course object by its unique ID.

        Args:
            item: The unique identifier (ID) of the Course to be retrieved.

        Returns:
            Course: The Course object associated with the provided unique ID.

        Note:
            This method allows you to access a Course object from the Courses
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._courses[item] 

    def add_item(self, key, value):
        """
        Add a Course object to the collection using a unique identifier (ID).

        Args:
            key: The unique identifier (ID) for the Course.
            value: The Course object to add to the collection.
        """
        self._courses[key] = value

#Course Requirement Classes
class CourseRequirement:
    """
    Represents all enrolment requirements of a Course.

    Attributes:
    - id (str): The course code
    - requirements (dict): A collection of CourseRequirementSpecific objects representing different requirements.
    """

    def __init__(self, id, requirements):
        """
        Initializes a CourseRequirement object with the course code and its requirements.

        Args:
        - id (str): The course code.
        - requirements (list): A list of CourseRequirementSpecific objects.
        """
        self.id = id
        self._requirements = {}

    def __str__(self):
        """
        Returns a string representation of the list of Department objects.

        Returns:
            str: A string with information for each Department.
        """

        formatted_string = "["

        for requirement in self._requirements:
            formatted_string += ("'{}: {}', ".format(self._requirements[requirement].id, self._requirements[requirement].criteria))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return(formatted_string)

    def add_requirement(self, course_requirement):
        """
        Add a CourseRequirementSpecific to the collection.

        Args:
            course_requirement (CourseRequirementSpecific): The CourseRequirementSpecific object to be added.
        """
        
        if course_requirement is not None:
           self._requirements[course_requirement._id] = course_requirement  # Use course ID as the key in the dictionary

    def add_requirements(self, course_requirements):
        """
        Add multiple course requirements to the collection.

        Args:
            course_requirements (list of CourseRequirementSpecific): A list of CourseRequirementSpecific objects to be added.
        """
        for requirement in course_requirements:
            self.add_requirement(requirement)

    def find_requirement_by_id(self, id):
        """
        Find a CourseRequirementSpecific by its unique identifier.

        Args:
            id (str): The unique course code of the CourseRequirementSpecific to search for.

        Returns:
            CourseRequirementSpecific or None: The CourseRequirementSpecific object if found, or None if not found.
        """
        return self._requirements.get(id, None)  # Use dictionary's get method

    def __iter__(self):
        """
        Make the CourseRequirement class iterable. This method returns an iterator.
        """
        self._current_index = 0
        self._requirements_list = list(self._requirements.values())
        return self

    def __next__(self):
        """
        Get the next CourseRequirementSpecific object in the iteration.
        """
        if self._current_index < len(self._requirements_list):
            course = self._requirements_list[self._current_index]
            self._current_index += 1
            return course
        raise StopIteration

    def __len__(self):
        """
        Get the number of CourseRequirementSpecific objects in the collection.

        Returns:
            int: The number of CourseRequirementSpecific objects in the collection.
        """
        return len(self._requirements)

    def __contains__(self, item):
        """
        Check if a CourseRequirementSpecific object is in the collection.

        Args:
            item: The CourseRequirementSpecific object to check for presence in the collection.

        Returns:
            bool: True if the CourseRequirementSpecific object is in the collection, False otherwise.
        """
        return item in self._requirements

    def __getitem__(self, item):
        """
        Retrieve a CourseRequirementSpecific object by its unique ID.

        Args:
            item: The unique course code (ID) of the CourseRequirementSpecific to be retrieved.

        Returns:
            CourseRequirementSpecific: The CourseRequirementSpecific object associated with the provided unique ID.

        Note:
            This method allows you to access a CourseRequirementSpecific object from the CourseRequirement
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._requirements[item] 

    def add_item(self, key, value):
        """
        Add a CourseRequirementSpecific object to the collection using a unique identifier (ID).

        Args:
            key: The unique identifier (ID) for the CourseRequirementSpecific.
            value: The CourseRequirementSpecific object to add to the collection.
        """
        self._requirements[key] = value

class CourseRequirementSpecific:
    """
    Represents a specific requirement for a course.

    Attributes:
    - type (str): The type of requirement, e.g., "PREREQUISITE".
    - criteria (str): The criteria for the requirement.
    """

    def __init__(self, type, criteria):
        """
        Initializes a CourseRequirementSpecific object with the type and criteria.

        Args:
        - type (str): The type of the requirement.
        - criteria (str): The criteria for the requirement.
        """
        self._id = type
        self._criteria = criteria
    @property
    def id(self):
        """
        Get the id attribute /or the requirement type.

        Returns:
        - string: The id attribute/requirement type.
        """
        return self._id
    
    @property
    def criteria(self):
        """
        Get the requiement rule /or criteria.

        Returns:
        - string: the rule /or criteria.
        """
        return self._criteria
    
    def __str__(self):
        return f"Type: {self._id} Criteria: {self._criteria}"

class CourseRequirements:
    """
    Represents a collection of course requirements.

    Attributes:
    - requirements (dict): A dictionary where course codes are keys, and CourseRequirement objects are values.
    """
    
    ALLREQUIREMENTS = None

    def __init__(self, course_requirements = None):
        """
        Initializes an empty CourseRequirements object.
        """
        self._requirements = {}  # Use a dictionary to store courses by ID
        if course_requirements is not None:
            self.add_course_requirements(course_requirements)

    @property
    def requirements(self):
        """
        Get the collection of CourseRequirement objects.

        Returns:
        - dict: The dictionary of all requirements.
        """
        return self._requirements

    @requirements.setter
    def requirements(self, course_requirement):
        """
        Add a CourseRequirement object to the collection.

        Args:
        - course_requirement (CourseRequirement): The CourseRequirement object to add.
        """
        self._requirements[course_requirement.course] = course_requirement

    def __str__(self):
        return f"{[course_code for course_code in self.requirements.keys()]}"

    def add_course_requirement(self, course_requirement):
        """
        Add a CourseRequirement to the collection.

        Args:
            course_requirement (CourseRequirement): The CourseRequirement object to be added.
        """
        
        if course_requirement is not None:
           self.requirements[course_requirement.id] = course_requirement  # Use course ID as the key in the dictionary

    def add_course_requirements(self, course_requirements):
        """
        Add multiple course requirements to the collection.

        Args:
            course_requirements (list of CourseRequirement): A list of CourseRequirement objects to be added.
        """
        for requirement in course_requirements:
            self.add_course_requirement(requirement)

    def find_course_requirement_by_id(self, id):
        """
        Find a CourseRequirement by its unique identifier.

        Args:
            id (str): The unique course code of the CourseRequirement to search for.

        Returns:
            CourseRequirement or None: The CourseRequirement object if found, or None if not found.
        """
        return self.requirements.get(id, None)  # Use dictionary's get method

    def __iter__(self):
        """
        Make the CourseRequirements class iterable. This method returns an iterator.
        """
        self._current_index = 0
        self._requirements_list = list(self._requirements.values())
        return self

    def __next__(self):
        """
        Get the next CourseRequirement object in the iteration.
        """
        if self._current_index < len(self._requirements_list):
            course = self._requirements_list[self._current_index]
            self._current_index += 1
            return course
        raise StopIteration

    def __len__(self):
        """
        Get the number of CourseRequirement objects in the collection.

        Returns:
            int: The number of CourseRequirement objects in the collection.
        """
        return len(self._requirements)

    def __contains__(self, item):
        """
        Check if a CourseRequirement object is in the collection.

        Args:
            item: The CourseRequirement object to check for presence in the collection.

        Returns:
            bool: True if the CourseRequirement object is in the collection, False otherwise.
        """
        return item in self._requirements

    def __getitem__(self, item):
        """
        Retrieve a CourseRequirement object by its unique ID.

        Args:
            item: The unique course code (ID) of the CourseRequirement to be retrieved.

        Returns:
            CourseRequirement: The CourseRequirement object associated with the provided unique ID.

        Note:
            This method allows you to access a CourseRequirement object from the CourseRequirements
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._requirements[item] 

    def add_item(self, key, value):
        """
        Add a CourseRequirement object to the collection using a unique identifier (ID).

        Args:
            key: The unique identifier (ID) for the CourseRequirement.
            value: The CourseRequirement object to add to the collection.
        """
        self._requirements[key] = value

#Course Department Classes
class Department:
    """
    Represents a Queens department with its attributes and provides properties for id, code, and name.

    Attributes:
        id (str): The unique identifier for the department.
        code (str): The department's code.
        name (str): The name of the department.

    Methods:
        __str__(): Returns a string representation of the Department instance.
    """
    def __init__(self, id, code, name):
        """
        Initializes a Department instance.

        Args:
            id (str): The unique identifier for the department.
            code (str): The department's code.
            name (str): The name of the department.
        """
        self._id = id
        self._code = code
        self._name = name

    @property
    def id(self):
        """
        str: The unique identifier for the department.
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Set the unique identifier for the department.

        Args:
            value (str): The new identifier for the department.
        """
        self._id = value

    @property
    def code(self):
        """
        str: The code of the department.
        """
        return self._code

    @code.setter
    def code(self, value):
        """
        Set the code of the department.

        Args:
            value (str): The new code for the department.
        """
        self._code = value

    @property
    def name(self):
        """
        str: The name of the department.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of the department.

        Args:
            value (str): The new name for the department.
        """
        self._name = value

    def __str__(self):
        """
        Returns a string representation of the department.

        Returns:
            str: A formatted string with department information.
        """
        #return f"Department ID: {self.id}, Department: {self.code}, Name: {self.name}"
        return f"{self.code}: {self.name}"

class Departments:
    """
    Represents a collection of department objects and provides methods to add and find departments.
    """
    def __init__(self):
        """
        Initializes a Departments instance with an empty list of departments.
        """
        self._departments = []
    
    def __init__(self, departments):
        """
        Initializes a Departments instance from a list of departments.
        """
        self._departments = departments

    @property
    def departments(self):
        """
        Get the list of Departments.
        """
        return self._departments

    @departments.setter
    def departments(self, value):
        """
        Set the list of Departments.

        Args:
            value (List): The new list of Departments.
        """
        self._departments = value


    def add_department(self, department):
        """
        Add a Department to the collection.

        Args:
            department (Department): The Department object to be added.
        """
        self._departments.append(department)

    def find_department_by_id(self, id):
        """
        Find a Department by its unique identifier.

        Args:
            id (str): The unique identifier of the Department to search for.

        Returns:
            Department or None: The Department object if found, or None if not found.
        """
        for department in self._departments:
            if department.id == id:
                return department
        return None  # Return None if Department with the given ID is not found

    def __str__(self):
        """
        Returns a string representation of the list of Department objects.

        Returns:
            str: A string with information for each Department.
        """

        formatted_string = "["

        for department in self._departments:
            formatted_string += ("'{}', ".format(department))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return(formatted_string)

    def __iter__(self):
        """
        Make the Department class iterable. This method returns an iterator.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Get the next Department object in the iteration.
        """
        if self._current_index < len(self._departments):
            department = self._departments[self._current_index]
            self._current_index += 1
            return department
        raise StopIteration

#Course Section Classes
class TermLevelSection:
    """
    Represents a parent section of a course during a specific Term.
    
    Note: Private: datalayer.py scope only
    """
    def __init__(self, id, year, term, department, course_code, course_name, units, campus, academic_level, course_sections):
        """
        Initializes a TermLevelSection instance.
        """
        self.TLS_id= id
        self.year = year
        self.term = term
        self.department = department
        self.course_code = course_code
        self.course_name = course_name
        self.units = units
        self.campus = campus
        self.academic_level = academic_level
        self.course_sections = course_sections
        self.courseid = ("{}-{}".format(department, course_code))
        
class Section(TermLevelSection):
    """
    Represents a specific course section with its attributes.

    Attributes:
        class_number (str): The unique identifier for the course section.
        combined_with (str): Information about combined sections, if applicable.
        dates (str): The dates when the course section is scheduled.
        enrollment_capacity (int): The maximum number of students that can enroll in the section.
        enrollment_total (int): The current number of students enrolled in the section.
        last_updated (str): Timestamp of the last update to the section information.
        section_name (str): The name of the course section.
        section_number (str): The section number.
        section_type (str): The type of the section (e.g., lecture, lab).
        waitlist_capacity (int): The maximum number of students that can be on the waitlist.
        waitlist_total (int): The current number of students on the waitlist.

    Methods:
        __str__(): Returns a string representation of the Section instance.
        has_conflict(other): Checks for date conflicts between two Section objects.
    """
    def __init__(self, class_number, combined_with, dates, enrollment_capacity, enrollment_total,
                 last_updated, section_name, section_number, section_type, waitlist_capacity, waitlist_total):
        
        #ENHERITED TermLevelSection
        
        #NEW
        self.id = section_name
        self.class_number = class_number
        self.combined_with = combined_with
        self.dates = dates
        self.enrollment_capacity = enrollment_capacity
        self.enrollment_total = enrollment_total
        self.last_updated = last_updated
        self.section_name = section_name
        self.section_number = section_number
        self.section_type = section_type
        self.waitlist_capacity = waitlist_capacity
        self.waitlist_total = waitlist_total
    
    def add_parent_section(self, id, year, term, department, course_code, course_name, units, campus, academic_level, course_sections):
        s = super().__init__(id, year, term, department, course_code, course_name, units, campus, academic_level, course_sections)
        self.id = f"{self.TLS_id}-{self._section_name}"
    
    def has_conflict(self, other):
        """
        Checks for date conflicts between two Section objects.

        This method compares the dates of the current Section object with another Section object
        to determine if there are any date and time conflicts. It iterates through the date
        schedules of both sections, and if it finds overlapping time slots on the same day,
        it indicates a conflict.

        Args:
            other (Section): Another Section object to compare against.

        Returns:
            bool: True if there is a date conflict between the two sections, False otherwise.

        Raises:
            ValueError: If the 'other' object is not an instance of the Section class.
        """
        if not isinstance(other, Section):
            raise ValueError("The other value must be a Section object")
        else:
                for date1 in self.dates:
                    for date2 in other.dates:
                        if not date1.is_tba() and not date2.is_tba():
                            start_time1 = datetime.strptime(date1.start_time, "%H:%M")
                            end_time1 = datetime.strptime(date1.end_time, "%H:%M")
                            start_time2 = datetime.strptime(date2.start_time, "%H:%M")
                            end_time2 = datetime.strptime(date2.end_time, "%H:%M")

                            if date1.day == date2.day:
                                # Check for time overlap
                                if start_time1 < end_time2 and end_time1 > start_time2:
                                    return True  # Conflict found
        return False
            
    @property
    def class_number(self):
        """
        Get the unique identifier for the course section.
        """
        return self._class_number

    @class_number.setter
    def class_number(self, value):
        """
        Set the unique identifier for the course section.
        """
        self._class_number = value

    @property
    def combined_with(self):
        """
        Get information about combined sections, if applicable.
        """
        return self._combined_with

    @combined_with.setter
    def combined_with(self, value):
        """
        Set information about combined sections, if applicable.
        """
        self._combined_with = value

    @property
    def dates(self):
        """
        Get the dates when the course section is scheduled.
        """
        return self._dates

    @dates.setter
    def dates(self, value):
        """
        Set the dates when the course section is scheduled.
        """
        self._dates = value

    @property
    def enrollment_capacity(self):
        """
        Get the maximum number of students that can enroll in the section.
        """
        return self._enrollment_capacity

    @enrollment_capacity.setter
    def enrollment_capacity(self, value):
        """
        Set the maximum number of students that can enroll in the section.
        """
        self._enrollment_capacity = value

    @property
    def enrollment_total(self):
        """
        Get the current number of students enrolled in the section.
        """
        return self._enrollment_total

    @enrollment_total.setter
    def enrollment_total(self, value):
        """
        Set the current number of students enrolled in the section.
        """
        self._enrollment_total = value

    @property
    def last_updated(self):
        """
        Get the timestamp of the last update to the section information.
        """
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value):
        """
        Set the timestamp of the last update to the section information.
        """
        self._last_updated = value

    @property
    def section_name(self):
        """
        Get the name of the course section.
        """
        return self._section_name

    @section_name.setter
    def section_name(self, value):
        """
        Set the name of the course section.
        """
        self._section_name = value

    @property
    def section_number(self):
        """
        Get the section number.
        """
        return self._section_number

    @section_number.setter
    def section_number(self, value):
        """
        Set the section number.
        """
        self._section_number = value

    @property
    def section_type(self):
        """
        Get the type of the section (e.g., lecture, lab).
        """
        return self._section_type

    @section_type.setter
    def section_type(self, value):
        """
        Set the type of the section (e.g., lecture, lab).
        """
        self._section_type = value

    @property
    def waitlist_capacity(self):
        """
        Get the maximum number of students that can be on the waitlist.
        """
        return self._waitlist_capacity

    @waitlist_capacity.setter
    def waitlist_capacity(self, value):
        """
        Set the maximum number of students that can be on the waitlist.
        """
        self._waitlist_capacity = value

    @property
    def waitlist_total(self):
        """
        Get the current number of students on the waitlist.
        """
        return self._waitlist_total

    @waitlist_total.setter
    def waitlist_total(self, value):
        """
        Set the current number of students on the waitlist.
        """
        self._waitlist_total = value

    def __str__(self):
        """
        Returns a string representation of the Section.

        Returns:
            str: A formatted string with Section information.
        """
        return(self.class_number)
    
class SectionDate:
    """
    Represents a SectionDate object with its attributes.

    Attributes:
        day (str): The day of the week for the section date.
        start_date (str): The start date of the section.
        end_date (str): The end date of the section.
        start_time (str): The start time of the section.
        end_time (str): The end time of the section.
        instructors (list): A list of instructors for the section date.
        location (str): The location where the section date takes place.

    Methods:
        __str__(self): Returns a string representation of the SectionDate instance.
    """
    def __init__(self, day, start_date, end_date, start_time, end_time, instructors, location):
        """
        Initializes a SectionDate with the provided attributes.

        Args:
            day (str): The day of the week for the section date.
            start_date (str): The start date of the section.
            end_date (str): The end date of the section.
            start_time (str): The start time of the section.
            end_time (str): The end time of the section.
            instructors (list): A list of instructors for the section date.
            location (str): The location where the section date takes place.
        """
        self.day = day
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.instructors = instructors
        self.location = location

    @property
    def day(self):
        """
        Get the day of the week for the section date.
        """
        return self._day

    @day.setter
    def day(self, value):
        """
        Set the day of the week for the section date.

        Args:
            value (str): The day of the week (e.g., 'Monday', 'Tuesday').
        """
        self._day = value

    @property
    def start_date(self):
        """
        Get the start date of the section.
        """
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        """
        Set the start date of the section.

        Args:
            value (str): The start date of the section.
        """
        self._start_date = value

    @property
    def end_date(self):
        """
        Get the end date of the section.
        """
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        """
        Set the end date of the section.

        Args:
            value (str): The end date of the section.
        """
        self._end_date = value

    @property
    def start_time(self):
        """
        Get the start time of the section.
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """
        Set the start time of the section.

        Args:
            value (str): The start time of the section.
        """
        self._start_time = value

    @property
    def end_time(self):
        """
        Get the end time of the section.
        """
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        """
        Set the end time of the section.

        Args:
            value (str): The end time of the section.
        """
        self._end_time = value

    @property
    def instructors(self):
        """
        Get the list of instructors for the section date.
        """
        return self._instructors

    @instructors.setter
    def instructors(self, value):
        """
        Set the list of instructors for the section date.

        Args:
            value (list): A list of instructors.
        """
        self._instructors = value

    @property
    def location(self):
        """
        Get the location where the section date takes place.
        """
        return self._location

    @location.setter
    def location(self, value):
        """
        Set the location where the section date takes place.

        Args:
            value (str): The location of the section date.
        """
        self._location = value

    def __str__(self):
        """
        Returns a string representation of the SectionDate.

        Returns:
            str: A formatted string with SectionDate information.
        """
        return (
            f"{self.day} {self.start_time} : {self.end_time}"
        )

    def is_tba(self):
        """
        Checks if the current date is 'TBA'.

        Returns:
            bool: True if this date is 'TBA', False otherwise.
        """
        return any(value == 'TBA' for value in [self.day, self.start_date, self.end_date, self.start_time, self.end_time])

class SectionDates:
    """
    Represents a collection of SectionDate objects with its attributes.

    Attributes:
        dates (list): The collection of SectionDate objet.

    Methods:
        __str__(self): Returns a string representation of the SectionDates instance.
    """
    def __init__(self):
        self._dates = []

    def __str__(self):
        """
        Returns a string representation of the list of SectionDates objects.

        Returns:
            str: A list with information for each SectionDate object.
        """
        formatted_string = "["

        for date in self._dates:
            formatted_string += ("'{}', ".format(date))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return formatted_string

    def add_date(self, date):
        """
        Add a SectionDate to the collection.

        Args:
            date (SectionDate): The SectionDate object to be added.
        """
        if date is not None:
            self._dates.append(date)
    
    def __iter__(self):
        """
        Make the SectionDates class iterable. This method returns an iterator.
        """
        self._date_iterator = iter(self._dates)
        return self

    def __next__(self):
        """
        Get the next SectionDate object in the iteration.
        """
        try:
            return next(self._date_iterator)
        except StopIteration:
            raise StopIteration

class Sections(Mapping):
    ALLSECTIONS = None
    """
    Represents a collection of Section objects with the ability to manage, search, and iterate through them.

    Attributes:
        sections (dict): A dictionary that stores Section objects in a 2D dictionary with the first level being the term 
            and the second level being the Sections by their unique IDs.

    Methods:
        add_sections(self, sections): Add multiple sections to the collection.
        add_section(self, section): Add a Section to the collection.
        find_section_by_id(self, id): Find a Section by its unique identifier.
        find_sections_by_course_code(self, code): Find all Sections over different terms by its course code.
        get_term_collection(self, term): Get a collection of Section objects during a specific term.
        __str__(self): Returns a string representation of the list of Section objects.
        __iter__(self): Make the Sections class iterable. This method returns an iterator.
        __next__(self): Get the next Section object in the iteration.
        __getitem__(self, item): Retrieve a Section object by its unique ID.
        __len__(self): Get the number of Section objects in the collection.
        __contains__(self, item): Check if a Section object is in the collection.
        __getitem__(self, item): Retrieve a Section object by its unique ID.
        add_items(self, key, value): Add a Section object to the collection using a unique identifier (ID).

    """
    
    def __init__(self, sections=None):
        """
        Initializes an empty Sections instance.
        """
        self._all_sections_by_term = None
        self._all_sections = {}
        
        self._has_fall = False
        self._has_winter = False
        self._has_summer = False
        
        self._fall_sections = {}
        self._winter_sections = {}
        self._summer_sections = {}
        
        if sections is not None:
            self.add_sections(sections)

    @property
    def all_sections_by_term(self):
        """
        Get the dictionary of Section objects per term.

        Returns:
            dict{dict}: A 2D dictonary of Section objects per term.
        """
        self._all_sections_by_term = {Term.FALL: self._fall_sections, Term.WINTER: self._winter_sections, Term.SUMMER: self._summer_sections}
        return self._all_sections_by_term

    @all_sections_by_term.setter
    def all_sections_by_term(self, value):
        """
        Set the dictionary of Section objects per term.

        Args:
            value (dict{dict}): The dictionary of Section objects per term.
        """
        if not isinstance(value, Mapping):
            if all(isinstance(m, Mapping) for m in value):
                self.all_sections_by_term = value
                
            else: raise ValueError("The value must be a 2D dictionary of Terms and CourseSection objects")
        else: raise ValueError("The value must be a 2D dictionary of Terms and CourseSection objects")

    def add_section(self, section):
        """
        Add a CourseSection to the collection in its correct Term collection.

        Args:
            section (CourseSection): The CourseSection object to be added.
        """
        term = section.term
        
        if term is Term.FALL or term == "FALL" or term == "Fall":
            section.term = Term.FALL
            self._fall_sections[section.id] = section
            self._all_sections[section.id] = section #add section to collection of all sections
            self._has_fall = True
            
        elif term is Term.WINTER or term == "WINTER" or term == "Winter":
            section.term = Term.WINTER
            self._winter_sections[section.id] = section
            self._all_sections[section.id] = section #add section to collection of all sections
            self._has_winter = True
        
        elif term is Term.SUMMER or term == "SUMMER" or term == "Summer":
            section.term = Term.SUMMER
            self._summer_sections[section.id] = section
            self._all_sections[section.id] = section #add section to collection of all sections
            self._has_summer = True
        
        else:
            raise ValueError("The CourseSection term attribute must be a Term object")

    def add_sections(self, sections):
        """
        Add multiple sections to the collection.

        Args:
            sections (list of Section): A list of Section objects to be added.
        """
        for section in sections:
            self.add_section(section)

    def find_section_by_id(self, id):
        """
        Find a Section by its unique identifier.

        Args:
            id (str): The unique identifier of the Section to search for.

        Returns:
            Section or None: The Section object if found, or None if not found.
        """
        
        return self._all_sections.get(id, None)
    
    def get_term_collection(self, term):
        """
        Get a collection of CourseSection objects during a specific term.

        Args:
            term (Term): The term collection to return.

        Returns:
            list or None: A list of the CourseSection objects of a specified Term if found, or None if the Term collection is not found.
        """
        if term is Term.FALL or term == "FALL" or term == "Fall":
            return list(self._fall_sections.values())
            
        elif term is Term.WINTER or term == "WINTER" or term == "Winter":
            return list(self._winter_sections.values())
        
        elif term is Term.SUMMER or term == "SUMMER" or term == "Summer":
            return list(self._summer_sections.values())
        
        else:
            raise ValueError("The term value must be a Term object")
            return None
    
    def is_offered(self, term):
        """
        Returns True if a Section is offered during a specific Term.

        Returns:
            bool: True of False.
        """

        if term is Term.FALL:
           return self._has_fall
            
        elif term is Term.WINTER:
           return self._has_winter
        
        elif term is Term.SUMMER:
           return self._has_summer
    
    def get_term_offerings(self):
        """
        Get a collection of Term objects during that represent all the tern offerings of Section.

        Returns:
            list: A list of Term Enums.
        """
        term_offerings = []
        if len(self._fall_sections) > 0:
            term_offerings.append(Term.FALL)
            
        if len(self._winter_sections) > 0:
            term_offerings.append(Term.WINTER)
        
        if len(self._summer_sections) > 0:
            term_offerings.append(Term.SUMMER)
        
        return term_offerings
    
    
    def __str__(self):
        """
        Returns a string representation of the Sections object.

        Returns:
            str: A string with information for each Section.
        """
        fall = []
        for v in self._fall_sections.values():
            fall.append(str(v))
        winter = []
        for v in self._winter_sections.values():
            winter.append(str(v))
        summer = []
        for v in self._summer_sections.values():
            summer.append(str(v))
        
        return f"Fall: {fall}, Winter: {winter}, Summer: {summer}"

    def __iter__(self):
        """
        Make the Sections class iterable. This method returns an iterator.
        """
        self._term_iterator = iter(self.all_sections_by_term)
        self._section_iterator = None
        return self

    def __next__(self):
        """
        Get the next Section object in the iteration.
        """
        if self._section_iterator is None:
            term = next(self._term_iterator)
            self._section_iterator = iter(self._all_sections_by_term[term].values())

        try:
            return next(self._section_iterator)
        except StopIteration:
            # If a term is exhausted, move to the next term
            term = next(self._term_iterator)
            self._section_iterator = iter(self._all_sections_by_term[term].values())
            return next(self._section_iterator)
    
    def __len__(self):
        """
        Get the number of CourseSection objects in the collection.

        Returns:
            int: The number of CourseSection objects in the collection.
        """
        return len(self._all_sections)

    def __contains__(self, item):
        """
        Check if a CourseSection object is in the collection.

        Args:
            item: The CourseSection object to check for presence in the collection.

        Returns:
            bool: True if the CourseSection object is in the collection, False otherwise.
        """
        return item in self._all_sections

    def __getitem__(self, item):
        """
        Retrieve a CourseSetion object by its unique ID.

        Args:
            item: The unique identifier (ID) of the CourseSection to be retrieved.

        Returns:
            CourseSection: The CourseSection object associated with the provided unique ID.

        Note:
            This method allows you to access a CourseSection object from the Sections
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._all_sections[item] 

    def add_item(self, value):
        """
        Add a CourseSection object to the collection using a unique identifier (ID).

        Args:
            value: The CourseSection object to add to the collection.
        """
        self.add_section(value)

#Student Classes
class Student:
    """
    Represents a specific student with their attributes.

    Attributes:
        - _name (str): The name of the student.
        - _academic_year (AcademicYear): The current academic year of the student.
        - _program (string): The program the student is enrolled in.
        - _completed_courses (Courses): A Courses object containing a collection of this students completed of courses.
        - _course_wish_list (Courses): A Courses object containing the courses this student wishes to enroll in this academic year.
        - _friends (Friends): A collection of Friend objects representing a students friends and their shared courses.

    Methods:
        __str__(): Returns a string representation of the Student instance.
    """
    def __init__(self, name, academic_year, program, completed_courses, course_wish_list, friends):
        """
        Initializes a Student instance.

        Args:
            _name (str): The name of the student.
            _academic_year (AcademicYear): The current academic year of the student.
            _program (string): The program the student is enrolled in.
            _completed_courses (Courses): A Courses object containing a collection of this students completed of courses.
            _course_wish_list (Courses): A Courses object containing the courses this student wishes to enroll in this academic year.
             _friends (Friends): A collection of Friend objects representing a students friends and their shared courses.

        """
        self.name = name
        self.academic_year = academic_year
        self.program = program
        self.completed_courses = completed_courses
        self.course_wish_list = course_wish_list
        self.friends = Friends()
    
    def __str__(self):
        """
        Returns a string representation of the Student.

        Returns:
            str: A formatted string with Student information.
        """

        if len(self._course_wish_list) > 0:
            formatted_wish_list = "["

            for course in self._course_wish_list:
                formatted_wish_list += ("'{}', ".format(course))
            
            formatted_wish_list = formatted_wish_list[:-2]
            formatted_wish_list += "]"

            return("{}:{}" .format(self.name, formatted_wish_list))

        else:
            return self.name

    @property
    def name(self):
        """
        Get the student name attribute.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the student name attribute.

        Args:
            value (String): a student name.
        """
        self._name = value

    @property
    def academic_year(self):
        """
        Get the academic year attribute.
        """
        return self._academic_year

    @academic_year.setter
    def academic_year(self, value):
        """
        Set the academic year attribute.

        Args:
            value (Union[str, AcademicYear]): A string representation of the academic year 
            or an AcademicYear Enum object representing the academic year to be set.
        """
        if not isinstance(value, AcademicYear):
            self._academic_year = AcademicYear(value)
        else:
            self._academic_year = value      

    @property
    def program(self):
        """
        Get the program attribute.
        """
        return self._program

    @program.setter
    def program(self, value):
        """
        Set the program attribute.

        Args:
            value (String): a program.
        """
        self._program = value

    @property
    def completed_courses(self):
        """
        Get the completed_courses attribute, a Courses object.
        """
        return self._completed_courses

    @completed_courses.setter
    def completed_courses(self, value):
        """
        Set the completed courses attribute.

        This setter method is used to set the completed courses attribute for an instance
        of this Student. It accepts a value that can be either a Courses object or a list
        of unique course identifiers (Course IDs) represented as strings. It then assigns
        this value to the private attribute _completed_courses.

        Args:
            value (Union[Courses, List[str]]): A Courses object containing completed courses
            or a list of unique Course IDs as strings representing completed courses.

        Note:
            - If the provided value is a Courses object, it is directly assigned to the
            _completed_courses attribute.
            - If the provided value is a list of Course IDs, it iterates through the list,
            retrieves the corresponding Course objects using Course IDs, and creates
            a new Courses object containing these courses before assigning it to
            _completed_courses.
        """
        if not isinstance(value, Courses):
            if all(isinstance(c, str) for c in value):
                courses = Courses()
                for c in value:
                    if c in Courses.ALLCOURSES and c+"A" not in Courses.ALLCOURSES:
                        courses.add_course(Courses.ALLCOURSES.find_course_by_id(c))
                    
                    # If course is full year and has A B terms
                    elif c+"A" in Courses.ALLCOURSES and c+"B" in Courses.ALLCOURSES:
                        first_term = Courses.ALLCOURSES.find_course_by_id(c+"A")
                        second_term = Courses.ALLCOURSES.find_course_by_id(c+"B")
                        courses.add_course(first_term)
                        courses.add_course(second_term)

                self._completed_courses = courses

            else:
                raise ValueError("The value must be a Courses object or a list of unique Course ID's")
        else:
            self._completed_courses = value        

    @property
    def course_wish_list(self):
        """
        Get the course_wish_list attribute, a Courses object.
        """
        return self._course_wish_list

    @course_wish_list.setter
    def course_wish_list(self, value):
        """
        Set the course wish list attribute.

        This setter method is used to set the course wish list attribute for an instance
        of this Student. It accepts a value that can be either a Courses object or a list of
        unique course IDs (strings). If the provided value is a list of course IDs, it
        creates a Courses object and adds the courses based on the IDs.

        Args:
            value (Union[Courses, List[str]]): A Courses object representing the course
            wish list or a list of unique course IDs (strings) to be added to the wish list.

        Note:
            - If the provided value is a Courses object, it is directly assigned to the
            _completed_courses attribute.
            - If the provided value is a list of Course IDs, it iterates through the list,
            retrieves the corresponding Course objects using Course IDs, and creates
            a new Courses object containing these courses before assigning it to
            _course_wish_list.
        """
        if not isinstance(value, Courses):
            if all(isinstance(c, str) for c in value):
                courses = Courses()
                for c in value:
                    if c in Courses.ALLCOURSES and c+"A" not in Courses.ALLCOURSES:
                        courses.add_course(Courses.ALLCOURSES.find_course_by_id(c))
                    
                    # If course is full year and has A B terms
                    elif c+"A" in Courses.ALLCOURSES and c+"B" in Courses.ALLCOURSES:
                        first_term = Courses.ALLCOURSES.find_course_by_id(c+"A")
                        second_term = Courses.ALLCOURSES.find_course_by_id(c+"B")
                        courses.add_course(first_term)
                        courses.add_course(second_term)

                self._course_wish_list = courses
            else:
                raise ValueError("The value must be a Courses object or a list of unique Course ID's")
        else:
            self._course_wish_list = value        

    @property
    def friends(self):
        """
        Get the friends attribute, a Friends object.
        """
        return self._friends

    @friends.setter
    def friends(self, value):
        """
        Set the friends attribute.

        Args:
            value (Friends): A Friends object representing a students friends
        """
        
        self._friends = value
        
    def has_friends(self):
        """
        Returns True if a Student has friends in which they wish to take courses with.

        Returns:
            bool: True if a Student has Friends in which they wish to take courses with, otherwise false
        """
        return (len(self.friends) > 0)
    
    def is_reciprocal(self, friend, course):
        """
        Returns True if the Friend of Student also wishes to take the same course with them.

        Args:
            friend (Friend): A Friend object, that exists in this Student's colletion of Friends
            course (Course): A Course object, that represents the Course both students might want to take.


        Returns:
            bool: True if the Friend of Student also wishes to take the same course with them, otherwise False.
        """
        
        #ensure the friend that is passed is indeed their friend and that the course preference is one that they wish to take.
        if friend in self.friends and course in self.course_wish_list:
            #get the student object of the friend, to see if this student exists as a friend to them'
            friends_of_friend = Students.ALLSTUDENTS[friend.name].friends
            
            #if there friendship is mutal, check if the course preference is mutal
            if self in friends_of_friend:
                return course in friends_of_friend[self.name].shared_courses
        
        return False
                
class Students(Mapping):
    """
    Represents a collection of Student objects with the ability to manage, search, and iterate through them.

    Attributes:
        students (dict): A dictionary that stores Student objects by their unique IDs.

    Methods:
        add_student(self, student): Add a Student to the collection.
        find_student_by_name(self, name): Find a Student by its unique identifier.
        __str__(self): Returns a string representation of the list of Student objects.
        __iter__(self): Make the Students class iterable. This method returns an iterator.
        __next__(self): Get the next Student object in the iteration.
        __getitem__(self, item): Retrieve a Student object by its unique ID.
        __len__(self): Get the number of Student objects in the collection.
        __contains__(self, item): Check if a Student object is in the collection.
        __getitem__(self, item): Retrieve a Student object by its unique ID.
        add_items(self, key, value): Add a Student object to the collection using a unique identifier (ID).

    """
    ALLSTUDENTS = None

    def __init__(self, students=None):
        """
        Initializes a Students instance with an optional dictionary of Student objects.

        Args:
            students (dict, optional): A dictionary of Student objects indexed by student name.
                Default is None, which creates an empty dictionary.
        """
        self._students = {}  # Use a dictionary to store students by name
        if students is not None:
            self.add_students(students)

    @property
    def students(self):
        """
        Get the list of Students.
        """
        return self._students

    @students.setter
    def students(self, value):
        """
        Set the list of Students.

        Args:
            value (List): The new list of Students.
        """
        self._students = value

    def add_student(self, student):
        """
        Add a student  to the collection.

        Args:
            student (Student): The Student object to be added.
        """
        if student is not None:
            self._students[student.name] = student  # Use student name as the key in the dictionary

    def add_students(self, students):
        """
        Add multiple students to the collection.

        Args:
            students (list of Students): A list of Student objects to be added.
        """
        for student in students:
            self.add_student(student)


    def find_student_by_name(self, name):
        """
        Find a Student object by its unique name.

        Args:
            id (str): The unique name of the Student to search for.

        Returns:
            Student or None: The Student object if found, or None if not found.
        """
        return self._students.get(name, None)

    def __str__(self):
        """
        Returns a string representation of the list of Student objects.

        Returns:
            str: A list with information for each Student.
        """

        formatted_string = "["

        for student in self._students:
            formatted_string += ("'{}', ".format(student))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return(formatted_string)

    def __iter__(self):
        """
        Make the Students class iterable. This method returns an iterator.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Get the next Student object in the iteration.
        """
        students_list = list(self._students.values())
        if self._current_index < len(students_list):
            student = students_list[self._current_index]
            self._current_index += 1
            return student
        raise StopIteration

    def __getitem__(self, item):
        """
        Retrieve a Student object by its unique ID.

        Args:
            item: The unique identifier (ID) of the Student to be retrieved.

        Returns:
            Student: The Student object associated with the provided unique ID.

        Note:
            This method allows you to access a Student object from the Students
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._students[item] 
    
    def __len__(self):
        """
        Get the number of Student objects in the collection.

        Returns:
            int: The number of Student objects in the collection.
        """
        return len(self._students)

    def __contains__(self, item):
        """
        Check if a Student object is in the collection.

        Args:
            item: The Student object to check for presence in the collection.

        Returns:
            bool: True if the Student object is in the collection, False otherwise.
        """
        return (item in self._students) or (item.name in self._students)

    def __getitem__(self, item):
        """
        Retrieve a Student object by its unique ID.

        Args:
            item: The unique identifier (ID) of the Student to be retrieved.

        Returns:
            Student: The Student object associated with the provided unique ID.

        Note:
            This method allows you to access a Student object from the Students
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._students[item] 

    def add_item(self, key, value):
        """
        Add a Stuent object to the collection using a unique identifier (ID).

        Args:
            key: The unique identifier (ID) for the Student.
            value: The Student object to add to the collection.
        """
        self._students[key] = value

#Freind Classes
class Friend():
    """
    Represents a specific friend with their attributes.

    Attributes:
        - _shared_courses (Courses): A Courses object containing the courses this friend wishes to share with a student this academic year.
        - _name (str): A students name

    Methods:
        __str__(): Returns a string representation of the Friend instance.
    """
    def __init__(self, name, shared_courses, student):
        """
        Initializes a Friend instance.

        Args:
            _shared_courses (Courses): A Courses object containing the courses this friend wishes to share with a student this academic year.
            _name (str): A students name
        """
        self.shared_courses = shared_courses
        self.name = name
        self.student = student # a link to a student object
        
    
    def __str__(self):
        """
        Returns a string representation of the Friend.

        Returns:
            str: A formatted string with Friend information.
        """

        formatted_shared_list = "["

        for course in self._shared_courses:
            formatted_shared_list += ("'{}', ".format(course))
        
        formatted_shared_list = formatted_shared_list[:-2]
        formatted_shared_list += "]"

        return("{}:{}" .format(self.name, formatted_shared_list))
    
    
    @property
    def name(self):
        """
        Get the student name attribute.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the student name attribute.

        Args:
            value (String): a student name.
        """
        self._name = value


    @property
    def shared_courses(self):
        """
        Get the shared_courses attribute, a Courses object.
        """
        return self._shared_courses

    @shared_courses.setter
    def shared_courses(self, value):
        """
        Set the shared course list attribute. #LEFT OFF

        This setter method is used to set the shared course  list attribute for an instance
        of a freind. It accepts a value that can be either a Courses object or a list of
        unique course IDs (strings). If the provided value is a list of course IDs, it
        creates a Courses object and adds the courses based on the IDs.

        Args:
            value (Union[Courses, List[str]]): A Courses object representing the shared course
            list or a list of unique course IDs (strings) to be added to the wish list.

        Note:
            - If the provided value is a Courses object, it is directly assigned to the
            _completed_courses attribute.
            - If the provided value is a list of Course IDs, it iterates through the list,
            retrieves the corresponding Course objects using Course IDs, and creates
            a new Courses object containing these courses before assigning it to
            _shared_courses.
        """
        if not isinstance(value, Courses):
            if all(isinstance(c, str) for c in value):
                courses = Courses()
                for c in value:
                    courses.add_course(Courses.ALLCOURSES.find_course_by_id(c))

                self._shared_courses = courses
            else:
                raise ValueError("The value must be a Courses object or a list of unique Course ID's")
        else:
            self._shared_courses = value        
        
class Friends(Mapping):
    """
    Represents a collection of Friend objects with the ability to manage, search, and iterate through them.

    Attributes:
        friends (dict): A dictionary that stores Friends objects by their unique IDs.

    Methods:
        add_friend(self, student): Add a Friend to the collection.
        find_friend_by_name(self, name): Find a Friend by its unique identifier.
        __str__(self): Returns a string representation of the list of Friend objects.
        __iter__(self): Make the Friends class iterable. This method returns an iterator.
        __next__(self): Get the next Friend object in the iteration.
        __getitem__(self, item): Retrieve a Friend object by its unique ID.
        __len__(self): Get the number of Friend objects in the collection.
        __contains__(self, item): Check if a Friend object is in the collection.
        __getitem__(self, item): Retrieve a Friend object by its unique ID.
        add_items(self, key, value): Add a Friend object to the collection using a unique identifier (ID).

    """
    ALLFRIENDS = None

    def __init__(self, friends=None):
        """
        Initializes a Friends instance with an optional dictionary of Friend objects.

        Args:
            friends (dict, optional): A dictionary of Friend objects indexed by friend name.
                Default is None, which creates an empty dictionary.
        """
        self._friends = {}  # Use a dictionary to store students by name
        if friends is not None:
            self.add_friends(friends)

    @property
    def friends(self):
        """
        Get the list of Friends.
        """
        return self._friends

    @friends.setter
    def friends(self, value):
        """
        Set the list of Friends.

        Args:
            value (List): The new list of Friends.
        """
        self._friends = value

    def add_friend(self, friend):
        """
        Add a friend to the collection.

        Args:
            friend (Friend): The Friend object to be added.
        """
        if friend is not None:
            self._friends[friend.name] = friend  # Use friend name as the key in the dictionary

    def add_students(self, friends):
        """
        Add multiple friends to the collection.

        Args:
            friends (list of Friends): A list of Friends objects to be added.
        """
        for friend in friends:
            self.add_friend(friend)


    def find_friend_by_name(self, name):
        """
        Find a Friend object by its unique name.

        Args:
            id (str): The unique name of the Friend to search for.

        Returns:
            Friend or None: The Friend object if found, or None if not found.
        """
        return self._friends.get(name, None)

    def __str__(self):
        """
        Returns a string representation of the list of Friend objects.

        Returns:
            str: A list with information for each Friend.
        """

        formatted_string = "["

        for friend in self._friends:
            formatted_string += ("'{}', ".format(friend))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return(formatted_string)

    def __iter__(self):
        """
        Make the Friends class iterable. This method returns an iterator.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Get the next Friend object in the iteration.
        """
        friends_list = list(self._friends.values())
        if self._current_index < len(friends_list):
            friend = friends_list[self._current_index]
            self._current_index += 1
            return friend
        raise StopIteration

    def __getitem__(self, item):
        """
        Retrieve a Friend object by its unique ID.

        Args:
            item: The unique identifier (ID) of the Friend to be retrieved.

        Returns:
            Friend: The Friend object associated with the provided unique ID.

        Note:
            This method allows you to access a Friend object from the Friends
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._friends[item] 
    
    def __len__(self):
        """
        Get the number of Friend objects in the collection.

        Returns:
            int: The number of Friend objects in the collection.
        """
        return len(self._friends)

    def __contains__(self, item):
        """
        Check if a Friend object is in the collection.

        Args:
            item: The Friend object to check for presence in the collection.

        Returns:
            bool: True if the Friend object is in the collection, False otherwise.
        """
        return (item in self._friends) or (item.name in self._friends)

    def __getitem__(self, item):
        """
        Retrieve a Friend object by its unique ID.

        Args:
            item: The unique identifier (ID) of the Friend to be retrieved.

        Returns:
            Friend: The Friend object associated with the provided unique ID.

        Note:
            This method allows you to access a Friend object from the Friends
            collection using its unique identifier. If the ID is not found, it
            will raise a KeyError.
        """
        return self._friends[item] 

    def add_item(self, key, value):
        """
        Add a Friend object to the collection using a unique identifier (ID).

        Args:
            key: The unique identifier (ID) for the Friend.
            value: The Friend object to add to the collection.
        """
        self._friends[key] = value

def mapDepartments(buildings_file):
    """
    Map data from a buildings.json JSON file to Department objects.

    Args:
        buildings_file (str): The path to the buildings.json JSON file.

    Returns:
        Departments: An instance of the Departments class containing a collection of Department objects.
    """
    with open(buildings_file, "r") as json_file:
        data = json.load(json_file)

    departments = []  # Create a list to store Department objects 

    for department_data in data:
        
        department = Department(
            department_data["id"],
            department_data["code"],
            department_data["name"]
        )
        departments.append(department)

    # Return a collection of Department objects
    return Departments(departments)

def mapRequirements(requirements_file):
    """
    Map data from a requirements.json JSON file to CourseRequirement objects.
    Links Course requirements to their respective Requirements object if a Requirements object has been initalized.

    Args:
        requirements_file (str): The path to the requirements JSON file.

    Returns:
        CourseRequirements: An instance of the CourseRequirements class containing a collection of CourseRequirement objects.
    """
    with open(requirements_file, "r") as json_file:
        data = json.load(json_file)

    # Iterate through the JSON data and create Requirement instances
    all_course_requirements = []  #create a list to store Requirement objects 
    for course_requirements in data:
        course_requirement = CourseRequirement(**course_requirements)
        all_course_requirements.append(course_requirement)
        all_specific_requirements = []
        
        for specifc_requirement in course_requirements["requirements"]:
            all_specific_requirements.append(CourseRequirementSpecific(**specifc_requirement))
            
        course_requirement.add_requirements(all_specific_requirements)

        course_obj_link = course_requirements["id"]
        course_obj = Courses.ALLCOURSES.find_course_by_id(course_obj_link)
        if course_obj is not None:
            course_obj.requirements = course_requirement


    # Return a collection of CourseRequirement objects and set the global ALLREQUIREMENTS attribute
    CourseRequirements.ALLREQUIREMENTS = CourseRequirements(all_course_requirements)
    return CourseRequirements.ALLREQUIREMENTS
    
def mapSections(sections_file):
    """
    Map data from a sections JSON file to CourseSection objects.
    Links Course sections to their respective Sections objects if a Sections object has been initalized.

    Args:
        sections_file (str): The path to the sections JSON file.

    Returns:
        CourseSections: An instance of the CourseSections class containing a collection of CourseSection objects.
    """
    with open(sections_file, "r") as json_file:
        data = json.load(json_file)
        
    # Iterate through the JSON data and create Section instances
    every_section = [] #create a list to store Section objects 
    for parent_section in data:
        course_obj_link = f"{parent_section['department']}-{parent_section['course_code']}"
        all_course_sections = Sections()
        for each_section in parent_section["course_sections"]:
            
            # A list of other class options besides standard lecture, all of these sections are ignored
            Unimplemented = ["Laboratory","Tutorial", "Seminar", "Online", "IndividualStudy", "Clinical", "Research", "Project", "Practicum", "Blended", "Exam", "Demonstration", "ThesisResearch", "FieldStudies"]
            
            if each_section["section_type"] == "Lecture": #if section type is Lecture add to list of Lectures, i.e. all_course_sections
                each_section_mapped = Section(**each_section)
                each_section_mapped.add_parent_section(**parent_section) #inialize the parent term section for the child
                each_section_mapped.dates = SectionDates()
                for date in each_section["dates"]:
                    each_section_mapped.dates.add_date(SectionDate(**date)) #link child date arrays to dates attribute
                all_course_sections.add_section(each_section_mapped)
                every_section.append(each_section_mapped)
            
        course_obj = Courses.ALLCOURSES.find_course_by_id(course_obj_link)
        if course_obj is not None:
            if len(course_obj.sections) == 0:
                course_obj.sections = all_course_sections
            else:
                course_obj.sections.add_sections(all_course_sections._all_sections.values())
    
    # Return a collection of Section objects and set the global ALLSECTIONS attribute
    Sections.ALLSECTIONS = Sections(every_section)
    return Sections.ALLSECTIONS

def mapCourses(courses_file):
    """
    Map data from a courses JSON file to Course objects. 

    Args:
        courses_file (str): The path to the courses JSON file.

    Returns:
        Courses: An instance of the Courses class containing a collection of Course objects.
    """
    with open(courses_file, "r") as json_file:
        data = json.load(json_file)

    # Iterate through the JSON data and create Course instances
    courses = []  #create a list to store course objects 
    for course_data in data:
        course = Course(**course_data)
        courses.append(course)



    # Return a collection of Course objects and set the global ALLCOURSES attribute
    Courses.ALLCOURSES = Courses(courses)
    return Courses.ALLCOURSES

def mapStudents(students_file):
    """
    Map data from a student JSON file to Students objects.
    Links Student courses to their respective Course objects if a Courses object has been initalized

    Args:
        students_file (str): The path to the students JSON file.

    Returns:
        Students: An instance of the Students class containing a collection of Student objects.
    """
    with open(students_file, "r") as json_file:
        data = json.load(json_file)

    all_students = []  # Create a list to store course objects 

    # Iterate through the JSON data and create Student instances
    for student_data in data:
        student = Student(**student_data)
        all_students.append(student)

    # Return a collection of CourseSection objects
    Students.ALLSTUDENTS = Students(all_students)
    
    mapFriends(data)
    return Students.ALLSTUDENTS

def mapFriends(student_data):
    """
    Map data from a student JSON file to Friendss objects.
    Links Student freinds to their respective Friends objects if a Students object has been initalized

    Args:
       students_file (str): The path to the students JSON file.

    Returns:
        None
        
    Raises:
        ValueError: A freind must exists as a Student object in the global Students.ALLSTUDENTS attribute before it can be initalized as a Friend object
    """
    for student in student_data:
        student_obj = Students.ALLSTUDENTS.find_student_by_name(student["name"])
        
        all_friends = Friends()
        for friend in student["friends"]:
            friend_student_obj = Students.ALLSTUDENTS.find_student_by_name(friend["name"])
            if friend_student_obj is not None:
                all_friends.add_friend(Friend(friend["name"], friend["shared_courses"], friend_student_obj))
            
            else:
                raise ValueError(f"a friend must exist as a student")
        
        student_obj.friends = all_friends

if __name__ == "__main__":
    pass
    