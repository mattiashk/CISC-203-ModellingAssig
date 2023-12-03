import json
from datetime import datetime, timedelta
import sat_solver

"""
Module for Timetable View mapping and JSON Serialization

This module defines classes for representing timetable views in the Nextjs app. It also and provides functions
to convert these classes into raw JSON.

Classes:
- TimeTableView: Represents a timetable for multiple students.
- StudentView: Represents a specific student's timetable.
- TermView: Represents a term within a specific student's timetable.
- CourseView: Represents a course in specific student's timetable.
- CourseDateView: Represents a course date for a specific student's timetable

Functions:
- map_week_days(date_obj): Maps week days to date objects starting from Sunday.
- create_json(solution, objects): Creates a JSON representation of the SAT solver's timetable solution.
"""


class TimeTableView:
    """
    Represents a collection of student timetables.

    Attributes:
    - students: A collection of StudentView objects representing the enrolled students.

    Methods:
    - to_dict(): Converts the TimeTableView object to a dictionary for JSON serialization.
    """
    def __init__(self):
        self.students = []
        
    def to_dict(self):
        return [student.to_dict() for student in self.students]

class StudentView:
    """
    Represents a student.

    Attributes:
    - student: The name of the student.
    - terms: A collection of TermView objects representing the terms the student is enrolled in.

    Methods:
    - to_dict(): Converts the StudentView object to a dictionary for JSON serialization.
    """
    def __init__(self, name):
        self.student = name
        self.terms = {}

    def to_dict(self):
        return {"student": self.student, "terms": [term.to_dict() for term in self.terms.values()]}


class TermView:
    """
    Represents a term in a specific student's timetable.

    Attributes:
    - term: The term ("FALL", "WINTER", "SUMMER").
    - courses: A list of CourseView objects representing the courses a student is enrolled in for the term.

    Methods:
    - to_dict(): Converts the TermView object to a dictionary for JSON serialization.
    """
    def __init__(self, term):
        self.term = term
        self.courses = []
    
    def to_dict(self):
        return {"term": str(self.term), "courses": [course.to_dict() for course in self.courses]}

class CourseView:
    """
    Represents a course in specific student's timetable.

    Attributes:
    - course: The course code of the course.
    - dates: A list of CourseDateView objects representing the weekly dates for the course.

    Methods:
    - set_dates(data): Maps the raw string date data to CourseDateView objects and sets the 'dates' attribute.
    - to_dict(): Converts the CourseView object to a dictionary for JSON serialization.
    """
    def __init__(self, course_name, dates):
        self.course = course_name
        self.dates = self.set_dates(dates)
        
    def set_dates(self, data):
        mapped_dates = []
        current_weekday_map = map_week_days(datetime.now().date())
        
        for date in data:
            if date != "TBA":
                try:
                    current_date = current_weekday_map[date.day]
                    start_time = datetime.strptime(date.start_time, "%H:%M").time()
                    end_time = datetime.strptime(date.end_time, "%H:%M").time()
                    
                    start = datetime.combine(current_date, start_time)
                    end = datetime.combine(current_date, end_time)
                    
                    new_date = CourseDateView(start, end, date.location)
                except:
                    new_date = CourseDateView("TBA", "TBA", date.location)
            else:
                new_date = CourseDateView("TBA", "TBA", date.location)
            mapped_dates.append(new_date)
            
        return mapped_dates
        

    def to_dict(self):
        return {"course": self.course, "dates": [date.to_dict() for date in self.dates]}

class CourseDateView:
    """
    Represents a course date for a specific student's timetable.

    Args:
        data (list): Collection of dates.

    Methods:
    - to_dict(): Converts the CourseDateView object to a dictionary for JSON serialization.

    """
    def __init__(self, start, end, location):
        self.starttime = start
        self.endtime = end
        self.location = location

    def to_dict(self):
        if self.starttime == "TBA" or self.starttime is None or self.endtime == "TBA" or self.endtime is None:
            return {"starttime": "TBA", "endtime": "TBA", "location": self.location}
        
        else:
            return {"starttime": self.starttime.strftime("%Y-%m-%dT%H:%M:%S"), "endtime": self.endtime.strftime("%Y-%m-%dT%H:%M:%S"), "location": self.location}

def map_week_days(date_obj):
    """
    Maps week days to date objects starting with Sunday.

    Args:
        date_obj (datetime.date): A date object.

    Returns:
        dict: A dictionary mapping week days to date objects.
    """
    
    # Adjusted calculation for the start of the week (Sunday)
    if date_obj.weekday() == 6:  #if it's Sunday
        sunday = date_obj
    else:  #any other day
        sunday = date_obj - timedelta(days=date_obj.weekday() + 1)

    week_days = {
        'Sunday': sunday,
        'Monday': sunday + timedelta(days=1),
        'Tuesday': sunday + timedelta(days=2),
        'Wednesday': sunday + timedelta(days=3),
        'Thursday': sunday + timedelta(days=4),
        'Friday': sunday + timedelta(days=5),
        'Saturday': sunday + timedelta(days=6),
    }

    return week_days

def create_json(solution, objects):
    """
    Creates a JSON representation of the SAT solver timetable solution based on the given solution and datalayer objects.

    Args:
        solution (dict): A dictionary representing the solution from the SAT solver.
        objects (dict): A dictionary containing the datalayer collections.

    Returns:
        dict: A JSON representation of the timetable.
    """
    
    if solution is not None:
        students = objects["students"]
        timetableview = TimeTableView() #initialize a new TimeTableView to hold the current solution
        
        for student in students:
            studentview = StudentView(student.name) #initialize a new StudentView to hold the current Student
            
            for course in student.course_wish_list:
                if solution[sat_solver.StudentEnrolledCourse(student, course)]:
                    offered_terms = course.sections.get_term_offerings()
                    
                    for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
                        termview = TermView(str(term)) #initialize a new TermView to hold the current Term
                        
                        if solution[sat_solver.StudentEnrolledCourseTerm(student, course, term)]:
                            term_offerings = course.sections.get_term_collection(term) #get course term offerings
                            
                            for section in term_offerings: #get the Section objects from the term_offering
                                if solution[sat_solver.StudentEnrolledCourseSection(student, course, term, section)]:

                                    courseview = CourseView(section.id, section.dates ) #initialize a new CourseView to hold the Section a student is enrolled in
                                    termview.courses.append(courseview)
                                    
                                    #print(f"{student.name} enrolled in {section.id} in term {str(term)}") #REMOVE
                                    
                        if termview.courses != []:
                            if term in studentview.terms:
                                studentview.terms[term].courses += termview.courses
                            else:
                                studentview.terms[term] = termview
            timetableview.students.append(studentview)

        # Serialize to JSON
        data = timetableview.to_dict()
    
    else:
        data = None
    return data
