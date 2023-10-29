import json

"""
Object-Oriented JSON Data Modeling

This Python file defines classes for representing Queens courses, Queens departments and Queens course sections , as well as a collection for courses, departmentsm and course sections.

Classes:
- Course: Represents a course with its attributes.
- Courses: Represents a course with its attributes.

- Department: Represents a department with its attributes and provides properties for id, code, and name.
- Departments: Represents a collection of department objects and provides methods to add and find departments.

- CourseSection: Represents a course sections with its attributes.
- Section: Represents a specific course section (i.e. 001) with its attributes.
- SectionDate: Represents a course section's date (i.e. class dates) with its attributes.
- CourseSections: Represents a collection of course section objects and provides methods to add and find course sections.


Author: [Hayden Jenkins]
Date: [28/10/23]

Example usage:
- Create instances of Course, Department and CourseSection.
- Create Collections of Course, Department and CourseSection.
"""

class Course:
    """
    Represents a Queens course with its attributes.

    Attributes:
        id (str): The course ID.
        department (str): The department offering the course.
        course_code (str): The code of the course.
        course_name (str): The name of the course.
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
    """
    def __init__(self, id, department, course_code, course_name, campus, description, grading_basis,
                 course_components, requirements, add_consent, drop_consent, academic_level,
                 academic_group, academic_org, units, CEAB):
        self.id = id
        self.department = department
        self.course_code = course_code
        self.course_name = course_name
        self.section = {} #a dictionary of Section object that is linked to this Course
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
    def section(self):
        """
        Get the dictionary of Section objects that are connected to the Course object.
        """
        return self._section

    @section.setter
    def section(self, section):
        """
        Set the section attribute to a dictionary of Section objects that are connected to this Course.

        Args:
            value (Section): The Section to set.

        Returns:
            None
        """
        self._section = section

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

    def add_section_link(self, section):
        """
        """
        term = section.term
        self._section[term] = section
#depreciated
class Courses_slow:
    """
    Represents a collection of course objects and provides methods to add and find courses.
    """
    def __init__(self):
        """
        Initializes a Courses instance with an empty list of courses.
        """
        self._courses = []
    
    def __init__(self, courses):
        """
        Initializes a Courses instance from a list of courses.
        """
        self._courses = courses

    @property
    def courses(self):
        """
        Get the list of Courses.
        """
        return self._courses

    @courses.setter
    def courses(self, value):
        """
        Set the list of Courses.

        Args:
            value (List): The new list of Courses.
        """
        self._courses = value


    def add_course(self, course):
        """
        Add a Course to the collection.

        Args:
            course (Course): The Course object to be added.
        """
        self._courses.append(course)

    def find_course_by_id(self, id):
        """
        Find a Course by its unique identifier.

        Args:
            id (str): The unique identifier of the Course to search for.

        Returns:
            Course or None: The Course object if found, or None if not found.
        """
        for course in self._courses:
            if course.id == id:
                return course
        return None  # Return None if Course with the given ID is not found

    def __str__(self):
        """
        Returns a string representation of the list of Course objects.

        Returns:
            str: A list with information for each Course.
        """
        formatted_string = "["

        for course in self._courses:
            formatted_string += ("'{}', ".format(course))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return(formatted_string)

    def __iter__(self):
        """
        Make the Courses class iterable. This method returns an iterator.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Get the next Course object in the iteration.
        """
        if self._current_index < len(self._courses):
            course = self._courses[self._current_index]
            self._current_index += 1
            return course
        raise StopIteration
class Courses:
    def __init__(self, courses=None):
        """
        Initializes a Courses instance with an empty dictionary of courses.
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

class CourseSection:
    """
    Represents a course section group with its attributes.

    Attributes:
        id (int): The identifier for the course section.
        year (int): The academic year in which the course section is offered.
        term (str): The term during which the course section is held (e.g., 'Spring', 'Fall').
        department (str): The department responsible for the course section.
        course_code (str): The unique code for the course.
        course_name (str): The name or title of the course.
        units (float): The number of course units.
        campus (str): The campus or location where the course section is conducted.
        academic_level (str): The academic level of the course section (e.g., 'Undergraduate', 'Graduate').
        course_sections (list): A list of subsections or components that make up the course section.

    Methods:
        __str__(): Returns a string representation of the CourseSection instance.

    """
    def __init__(self, id, year, term, department, course_code, course_name, units, campus, academic_level, course_sections):
        self.id = id
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
    
    @property
    def id(self):
        """
        Get the ID of the course section.
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Set the ID of the course section.
        """
        self._id = value

    @property
    def year(self):
        """
        Get the year of the course section.
        """
        return self._year

    @year.setter
    def year(self, value):
        """
        Set the year of the course section.
        """
        self._year = value

    @property
    def term(self):
        """
        Get the term of the course section.
        """
        return self._term

    @term.setter
    def term(self, value):
        """
        Set the term of the course section.
        """
        self._term = value

    @property
    def department(self):
        """
        Get the department of the course section.
        """
        return self._department

    @department.setter
    def department(self, value):
        """
        Set the department of the course section.
        """
        self._department = value

    @property
    def course_code(self):
        """
        Get the course code of the course section.
        """
        return self._course_code

    @course_code.setter
    def course_code(self, value):
        """
        Set the course code of the course section.
        """
        self._course_code = value

    @property
    def course_name(self):
        """
        Get the course name of the course section.
        """
        return self._course_name

    @course_name.setter
    def course_name(self, value):
        """
        Set the course name of the course section.
        """
        self._course_name = value

    @property
    def units(self):
        """
        Get the number of units of the course section.
        """
        return self._units

    @units.setter
    def units(self, value):
        """
        Set the number of units of the course section.
        """
        self._units = value

    @property
    def campus(self):
        """
        Get the campus of the course section.
        """
        return self._campus

    @campus.setter
    def campus(self, value):
        """
        Set the campus of the course section.
        """
        self._campus = value

    @property
    def academic_level(self):
        """
        Get the academic level of the course section.
        """
        return self._academic_level

    @academic_level.setter
    def academic_level(self, value):
        """
        Set the academic level of the course section.
        """
        self._academic_level = value

    @property
    def course_sections(self):
        """
        Get the course sections of the course section.
        """
        return self._course_sections

    @course_sections.setter
    def course_sections(self, value):
        """
        Set the course sections of the course section.
        """
        self._course_sections = value

    @property
    def courseid(self):
        """
        Get the course id of the course section.
        """
        return self._courseid

    @courseid.setter
    def courseid(self, value):
        """
        Set the course id of the course section.
        """
        self._courseid = value


    def __str__(self):
        """
        Returns a string representation of the CourseSection.

        Returns:
            str: A formatted string with CourseSection information.
        """
        return f"{self.id}"
class Section:
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
    """
    def __init__(self, class_number, combined_with, dates, enrollment_capacity, enrollment_total,
                 last_updated, section_name, section_number, section_type, waitlist_capacity, waitlist_total):
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
    Represents a course section with its attributes.

    Attributes:
        id (str): The unique identifier for the course section.
        year (int): The year in which the course section is offered.
        term (str): The term in which the course section is offered (e.g., 'Spring', 'Fall').
        department (str): The department offering the course section.
        course_code (str): The code of the course section.
        course_name (str): The name of the course section.
        units (float): The number of units associated with the course section.
        campus (str): The campus where the course section is located.
        academic_level (str): The academic level of the course section (e.g., 'Undergraduate', 'Graduate').
        course_sections (list): A list of course sections if the course has multiple sections.

    Methods:
        __str__(self):
            Returns a string representation of the CourseSection instance.

    """
    def __init__(self, day, end_date, end_time, instructors, location, start_date, start_time):
        self.day = day
        self.end_date = end_date
        self.end_time = end_time
        self.instructors = instructors
        self.location = location
        self.start_date = start_date
        self.start_time = start_time

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
        """
        self._day = value

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
        """
        self._end_date = value

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
        """
        self._location = value

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
        """
        self._start_date = value

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
        """
        self._start_time = value

    def __str__(self):
        """
        Returns a string representation of the SectionDate.

        Returns:
            str: A formatted string with SectionDate information.
        """
        return (
            f"{self.day} {self.start_time} : {self.end_time} {self.instructors} {self.location}"
        )
#depreciated
class Sections_slow:
    """
    Represents a collection of Section objects and provides methods to add and find Section.
    """
    def __init__(self):
        """
        Initializes a Section instance with an empty list of Sections.
        """
        self._sections = []
    
    def __init__(self, sections):
        """
        Initializes a Section instance from a list of Sections.
        """
        self._sections = sections

    @property
    def sections(self):
        """
        Get the list of Sections.
        """
        return self._sections

    @sections.setter
    def sections(self, value):
        """
        Set the list of Sections.

        Args:
            value (List): The new list of Sections.
        """
        self._sections = value


    def add_section(self, section):
        """
        Add a Section to the collection.

        Args:
            section (Section): The Section object to be added.
        """
        self._sections.append(section)

    def find_section_by_id(self, id):
        """
        Find a Section by its unique identifier.

        Args:
            id (str): The unique identifier of the Section to search for.

        Returns:
            Section or None: The Section object if found, or None if not found.
        """
        for section in self._sections:
            if section.id == id:
                return section
        return None  # Return None if Section with the given ID is not found

    def __str__(self):
        """
        Returns a string representation of the list of Section objects.

        Returns:
            str: A string with information for each Section.
        """

        formatted_string = "["

        for section in self._sections:
            formatted_string += ("'{}', ".format(section))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return(formatted_string)

    def __iter__(self):
        """
        Make the Sections class iterable. This method returns an iterator.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Get the next Section object in the iteration.
        """
        if self._current_index < len(self._sections):
            section = self._sections[self._current_index]
            self._current_index += 1
            return section
        raise StopIteration
class Sections:
    """
    Represents a collection of Section objects and provides methods to add and find Section.
    """
    def __init__(self, sections=None):
        self._sections = {"Winter": {}, "Fall": {}, "Summer": {}}
        if sections is not None:
            self.add_sections(sections)

    @property
    def sections(self):
        """
        Get the list of Section objects per term.

        Returns:
            list: A list of Section objects per term.
        """
        return self._sections

    @sections.setter
    def sections(self, key, value):
        """
        Set the list of Section objects per term.

        Args:
            value (list of Section): The new list of Section objects for a term.
        """
        self._sections[key] = {section.id: section for section in value}

    def add_section(self, section):
        """
        Add a Section to the collection.

        Args:
            section (Section): The Section object to be added.
        """
        term = section.term
        self._sections[term][section.courseid] = section

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
        return self._sections.get(id, None)
    
    def find_sections_by_course_code(self, code):
        """
        Find all Sections over different terms by its course code.

        Args:
            id (str): The course code of the Section to search for.

        Returns:
            List or None: A list of the Section objects if found, or None if not found.
        """
        '''
        matching_courses = []
        for term, term_courses  in self.sections.items():
                for course, course_obj in term_courses.items():
                        if course_obj.courseid == code:
                            matching_courses.append(course_obj)
        return matching_courses
        '''
        matching_courses = []
        for term, term_courses  in self.sections.items():
            if code in self.sections[term]:
                matching_courses.append(self.sections[term][code])
        return matching_courses

    def __str__(self):
        """
        Returns a string representation of the list of Section objects.

        Returns:
            str: A string with information for each Section.
        """
        formatted_string = "["

        for section in self._sections.values():
            formatted_string += ("'{}', ".format(section))
        
        formatted_string = formatted_string[:-2]
        formatted_string += "]"
        
        return formatted_string

    def __iter__(self):
        """
        Make the Sections class iterable. This method returns an iterator.
        """
        self._term_iterator = iter(self._sections)
        self._section_iterator = None
        return self

    def __next__(self):
        """
        Get the next Section object in the iteration.
        """
        if self._section_iterator is None:
            term = next(self._term_iterator)
            self._section_iterator = iter(self._sections[term].values())

        try:
            return next(self._section_iterator)
        except StopIteration:
            # If a term is exhausted, move to the next term
            term = next(self._term_iterator)
            self._section_iterator = iter(self._sections[term].values())
            return next(self._section_iterator)
        


class Student:
    """
    Represents a specific student with their attributes.

    Attributes:

    Methods:
        __str__(): Returns a string representation of the Student instance.
    """
    def __init__(self, name, courses):
        self._name = name
        self._courses_str = courses
        self._courses = None #a Courses object 
    
    def __str__(self):
        """
        Returns a string representation of the Student.

        Returns:
            str: A formatted string with Student information.
        """

        formatted_courses = "["

        for course in self._courses:
            formatted_courses += ("'{}', ".format(course))
        
        formatted_courses = formatted_courses[:-2]
        formatted_courses += "]"

        return("{}:{}" .format(self.name, formatted_courses))

    @property
    def courses(self):
        """
        Get the Courses object.
        """
        return self._courses

    @courses.setter
    def courses(self, value):
        """
        Set the couses attribute to a Courses objects.

        Args:
            value (Courses): a Courses object.
        """
        if not isinstance(value, (Courses, type(None))):
            raise ValueError("The value must be a Courses object or None")
        self._courses = value        

    @property
    def courses_str(self):
        """
        Get the list of courses as as list of strings.
        """
        return self._courses_str

    @courses_str.setter
    def courses_str(self, value):
        """
        Set the couses_str attribute to a list of course id's.

        Args:
            value (List): a list of strings.
        """
        self._courses_str = value        

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
class Students:
    """
    Represents a collection of Student objects and provides methods to add and find Students.
    """
    def __init__(self):
        """
        Initializes a CourseSections instance with an empty list of Students.
        """
        self._students = []
    
    def __init__(self, students):
        """
        Initializes a Students instance from a list of Students.
        """
        self._students = students

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


    def add_student(self, value):
        """
        Add a Student to the collection.

        Args:
            value (Student): The Student object to be added.
        """
        self.students.append(value)

    def find_student_by_id(self, name):
        """
        Find a Student object by its unique name.

        Args:
            id (str): The unique name of the Student to search for.

        Returns:
            Student or None: The Student object if found, or None if not found.
        """
        for student in self._students:
            if student.name == name:
                return student
        return None  # Return None if Student with the given name is not found

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
        if self._current_index < len(self._students):
            student = self._students[self._current_index]
            self._current_index += 1
            return student
        raise StopIteration


def mapDepartments(buildings_file):
    """
    Map data from a buildings JSON file to Department objects.

    Args:
        buildings_file (str): The path to the buildings JSON file.

    Returns:
        Departments: An instance of the Departments class containing a list of Department objects.
    """
    with open(buildings_file, "r") as json_file:
        data = json.load(json_file)

    departments = []  # Create a list to store course objects 

    for department_data in data:
        
        department = Department(
            department_data["id"],
            department_data["code"],
            department_data["name"]
        )
        departments.append(department)

    # Return a list of Department objects
    return Departments(departments)

def mapSections(sections_file):
    """
    Map data from a sections JSON file to CourseSection objects.

    Args:
        sections_file (str): The path to the sections JSON file.

    Returns:
        CourseSections: An instance of the CourseSections class containing a list of CourseSection objects.
    """
    with open(sections_file, "r") as json_file:
        data = json.load(json_file)

    all_courses = []  # Create a list to store course objects 
    # Iterate through the JSON data and create CourseSection instances
    for course_section_data in data:
        course_section = CourseSection(**course_section_data)

        term = course_section.term
        code = course_section.course_code

        all_course_sections = []
        # Iterate through the CourseSection JSON data and create Course instances
        for section_data in course_section.course_sections:
            #course_section.course_sections.append(Section(**section_data))
            section = Section(**section_data)
            all_course_sections.append(section)

            all_section_dates = []
            # Iterate through the Section JSON data and create SectionDate instances
            for course_section_data in section.dates:
                #course_section.course_sections.dates.append(SectionDate(**course_section_data))
                all_section_dates.append(SectionDate(**course_section_data))
            
            section.dates = all_section_dates #map list of Dates class to Parent Section Class attribute dates
        course_section.course_sections = all_course_sections #map list of Section classes to Parent CourseSection Class attribute course_sections

        #all_courses[term][code] = (course_section)
        all_courses.append(course_section)

    # Return a list of Section objects
    return Sections(all_courses)

def mapCourses(courses_file, mapped_sections = None):
    """
    Map data from a courses JSON file to Course objects.
    Links student courses to their respective Section objects if a Sections object is passed

    Args:
        courses_file (str): The path to the courses JSON file.
        (optional) mapped_sections (Sections): The Sections object containing all Section objects

    Returns:
        Courses: An instance of the Courses class containing a list of Course objects.
    """
    with open(courses_file, "r") as json_file:
        data = json.load(json_file)

    courses = []  # Create a list to store course objects 

    # Iterate through the JSON data and create Course instances
    for course_data in data:
        course = Course(**course_data)
        courses.append(course)

        #if a Sections object is passed then create the required links
        if mapped_sections is not None:
            for section in mapped_sections.find_sections_by_course_code(course.id):
                course.add_section_link(section)


    # Return a list of Course objects
    return Courses(courses)

def mapStudents(students_file, mapped_courses = None):
    """
    Map data from a student JSON file to Students objects.
    Links student courses to their respective Course objects if a Courses object is passed

    Args:
        students_file (str): The path to the students JSON file.
        (optional) mapped_courses (Courses): The Courses object containing all Course objects

    Returns:
        Students: An instance of the Students class containing a list of Student objects.
    """
    with open(students_file, "r") as json_file:
        data = json.load(json_file)

    all_students = []  # Create a list to store course objects 

    # Iterate through the JSON data and create Student instances
    for student_data in data:  
        student = Student(student_data["name"], student_data["courses"])
        all_students.append(student)

        #if a Courses object is passed then create the required links
        if mapped_courses is not None:
            student_courses = []
            for course in student.courses_str:
                student_courses.append(mapped_courses.find_course_by_id(course))

            student.courses = Courses(student_courses)

    # Return a list of CourseSection objects
    return Students(all_students)

#Depreciated
def link_sections_to_courses(sections, courses):
    """
    Links every Course object in course (a list of Courses) to a Section object in sections (a list of Courses) that share
    a unique identifier

    Args:
        sections ([Section]): The list of Section objects.
        courses ([Course]): The list of Course objects.

    Returns:
        None
    """
    for course in courses:
        course_id = course.id
        linked_section = sections.find_section_by_id(course_id)
        if linked_section is not None:
            course.add_section_link(linked_section)
            print("linked Course: {} to Section: {}".format(course_id, linked_section.id))

#Depreciated
def link_courses_to_students(students, courses):
    """
    Links every Student object in students (a list of Student objects) list of courses to the a specific Course object in courses (a list of Course objects).
    using a unique identifier

    Args:
        students ([Student]): The list of Student objects.
        courses ([Course]): The list of Course objects.

    Returns:
        None
    """

    linked_course_list = []
    for student in students:
        for course_id in student.courses_str:
            linked_student_course_pref = courses.find_course_by_id(course_id)
            if linked_student_course_pref is not None and linked_student_course_pref not in linked_course_list:
                linked_course_list.append(linked_student_course_pref)
        student.courses = Courses(linked_course_list)

if __name__ == "__main__":
    pass