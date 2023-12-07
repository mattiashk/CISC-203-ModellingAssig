## All test datasets used in the SHEDULE SENSEI

### Test Cases Summary

1. **test-medium-general**: Full course load for a first-year student.
2. **test-medium-friendship**: Full course load for two first-year friends.
3. **test-small-friendship-01**: Two friends, each with 2 courses, no conflicts.
4. **test-full-year-course**: A single full-year course across terms A and B.
5. **test-tbd-course**: Course without specified dates or times.
6. **test-prereq-satisfied**: Course with all prerequisites satisfied.
7. **test-prereq-not-satisfied**: Course with partially unmet prerequisites.
8. **test-prereq-not-satisfied-fullyear**: Course with unmet prerequisites including a full-year course, *no solution*.
9. **test-coreq-satisfied**: Course with met corequisites from previous year.
10. **test-coreq-satisfied-02**: Course requiring its non-satisfied corequisite.
11. **test-coreq-satisfied-03**: Course with non-satisfied corequisite and its prerequisite.
12. **test-coreq-complex**: Complex scenario with multiple unmet corequisites and prerequisites.
13. **test-exclusion**: Course with an exclusion criterion.
14. **test-exclusion2**: Course with an already taken exclusion *no solution*.
15. **your-custom-test-case**: An empty data set that you can configure.
16. **complete-large-test-case**: A complete data set containing all possible courses and sections (but no student data).


### How To Create Custom Test Cases
 **Identify Required Data**: 
  Determine the necessary courses, course sections, and course requirements.

- **Create Student Data**: 
  In `students.json`, create the student profiles, making sure to include course wish lists and completed courses.

- **Gather Course Data**: 
  Utilize the course code's from the student's course data, extract matching courses from `reference/courses.json` and add them to the `courses.json` .

- **Select Section Data**: 
  Match the course code from the student's course data and extract matching sections for each term from `reference/sections.json` and add them to the `sections.json`.

- **Compile Requirements**: 
  Extract requirements from `reference/requirements.json` or create new requirements and add them to the  `requirements.json`.

- **Create Sub-files**: 
  Save the `.json` files and update the `tests.config.json` in your root project folder with your newly created test case.
