    # #CONSTRAINT 0.1 - One Term Per Course Limit
    # #For every student and course, they can be enrolled in the course during only one term ex: one of "Fall", "Winter", "Summer" depending on a courses offering.
    # for student in students:
    #     for course in student.course_wish_list:
            
    #         ENROLLED_COURSE_TERM = []
            
    #         offered_terms = course.sections.get_term_offerings()
    #         for term in [datalayer.Term.FALL, datalayer.Term.WINTER, datalayer.Term.SUMMER]: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
    #             if term in offered_terms:
    #                 ENROLLED_COURSE_TERM.append(StudentEnrolledCourseTerm(student, course, term))
                
    #             #If the course is not offered in a term you can't take it in that term.
    #             else: 
    #                 constraint.add_none_of(E, [StudentEnrolledCourseTerm(student, course, term)])
            
    #         if len(ENROLLED_COURSE_TERM) > 0:
    #             constraint.add_at_most_one(E, ENROLLED_COURSE_TERM)
    #         else:
    #             warn(f"no sections have been declared for {course}, this may be something you forgot to do.")


    # #CONSTRAINT 2 - One Section Per Course Limit
    # #For every student and course, they can be enrolled in exactly one section of a course.
    # for student in students:
    #     for course in student.course_wish_list:
    #         offered_terms = course.sections.get_term_offerings()
    #         for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
    #             term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
    #             ENROLLED_COURSE_SECTIONS = [] #a list of all sections during a term for a particular course
                
    #             for section in term_offerings: #get the Section objects from the term_offering
    #                 ENROLLED_COURSE_SECTIONS.append(StudentEnrolledCourseSection(student, course, term, section))
                    
    #             ENROLLED_COURSE_SECTIONS_OPTIONS = Or(ENROLLED_COURSE_SECTIONS)
    #             E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> ENROLLED_COURSE_SECTIONS_OPTIONS)
                    
    #             #constraint.add_at_most_one(E, ENROLLED_COURSE_SECTIONS) #BUG
    
    
    # #CONSTRAINT 3 - NOT Course -> Not Term, Not Section
    # #For every student and every course in a students wishlist, if a student isn't enrolled in a course, then a student cannot be enrolled in any of a courses sections over any of the terms
    # for student in students:
    #     for course in student.course_wish_list:
    #         offered_terms = course.sections.get_term_offerings()
    #         for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
    #             term_offerings = course.sections.get_term_collection(term)#get course term offerings
                
    #             E.add_constraint(StudentEnrolledCourseTerm(student, course, term) >> StudentEnrolledCourse(student, course))


    # #CONSTRAINT 4 - Not Term Course -> Not Term Course Sections
    # #For every student and course, if they are enrolled in a course in a specific term they must be taking the course during that term.
    # for student in students:
    #     for course in student.course_wish_list:
    #         offered_terms = course.sections.get_term_offerings()
    #         for term in offered_terms: #loop over "WINTER", "SUMMER", "FALL" terms depending on course offering
    #             term_offerings = course.sections.get_term_collection(term)#get course term offerings
    #             for section in term_offerings: #get the Section objects from the term_offering

    #                 E.add_constraint(StudentEnrolledCourseSection(student, course, term, section) >> StudentEnrolledCourseTerm(student, course, term))
     