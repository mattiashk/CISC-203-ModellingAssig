    #CONSTRAINT 12 - If students are friends and wish to be enrolled in the same course, they may. If and only if there are no prior restrictions that affect them both.
    for student in students:
        if student.has_friends():
            for friend in student.friends:
                for course in friend.shared_courses:
                    if student.is_reciprocal(friend, course): #if the friendship and course selection is mutual
                        
                        term_options = [] #the term options 2 students can take a course in
                        for term in datalayer.Term:
                            term_offerings_course = course.sections.get_term_collection(term)
                            term_options.append(StudentEnrolledCourseTerm(student, course, term) & StudentEnrolledCourseTerm(friend, course, term))
                            
                            section_options = [] #the term options 2 students can take a course in
                            for section in term_offerings_course:
                                section_options.append(StudentEnrolledCourseSection(student, course, term, section) & StudentEnrolledCourseSection(friend, course, term, section))
                        
                        common_term = Or(term_options)
                        common_section = Or(section_options)
                            
                        E.add_constraint((StudentEnrolledCourse(student, course) & StudentEnrolledCourse(friend, course) & common_term ) >> (common_section))