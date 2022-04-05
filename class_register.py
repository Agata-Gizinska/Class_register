#!/usr/bin/python3

import datetime
import csv
import argparse


class Register:
    """
    A parent class representing a register.

    Attributes:
    -------------
    name : str
        The name of the register
    file : str
        The name of the .csv file containing the register

    Methods:
    -------------
    read_rows_in_register \n
    print_register

    Subclasses:
    -------------
    ClassroomRegister \n
    StudentRegister \n
    CourseRegister
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self.file = None

    def __repr__(self):
        return self.name

    def read_rows_in_register(self):
        """Read all lines in the register and return a list of rows."""
        with open(self.file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            rows = []
            for row in reader:
                rows.append(row)
            return rows

    def print_register(self):
        """Print all current content of a register."""
        with open(self.file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                print(row)


class ClassroomRegister(Register):
    """
    A child class of class Register representing the Classroom Register.

    Attributes:
    -------------
    name : str
        The name of the register
    file : str
        The name of the file containing the register, overrides parent class

    Methods:
    -------------
    is_classroom_in_register(classroom) \n
    extract_classroom_info(classroom, info) \n
    new_classroom(classroom) \n
    add_student_to_classroom(student, classroom) \n
    change_student_status(student, action)
    """

    def __init__(self):
        super().__init__()
        self.file = 'classrooms.csv'

    def is_classroom_in_register(self, classroom):
        """Check if a classroom is in the Classroom Register."""
        rows = self.read_rows_in_register()
        for row in rows:
            if classroom in row.get('Class name'):
                start_year = row.get('Start year')
                end_year = row.get('End year')
                # Strip strings from redundant characters
                students = row.get('Students').strip("[]")
                students = students.replace("\'", "").split(", ") \
                    if students else []
                graduates = row.get('Graduates').strip("[]")
                graduates = graduates.replace("\'", "").split(", ") \
                    if graduates else []
                dropout = row.get('Dropout').strip("[]")
                dropout = dropout.replace("\'", "").split(", ") \
                    if dropout else []
                classroom = Classroom(start_year, end_year, students,
                                      graduates, dropout)
                return classroom
            else:
                continue

    def extract_classroom_info(self, classroom, info):
        """Extract a specified kind of information from the Classroom
        Register."""
        fieldnames = ['Class name', 'Start year', 'End year', 'Students',
                      'Graduates', 'Dropout']
        searched_index = info.index() if info in fieldnames else None
        rows = self.read_rows_in_register()
        for row in rows:
            if classroom in row.get('Class name'):
                searched_info = row.get(fieldnames[searched_index])
                return searched_info
            else:
                continue

    def new_classroom(self, classroom):
        """Add a new classroom into the Classroom Register."""
        with open(self.file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            classroom_name = classroom.name
            start_year = classroom.start_year
            end_year = classroom.end_year
            students = classroom.student_list
            graduates = classroom.graduates
            dropout = classroom.dropout_list
            writer.writerow([classroom_name, start_year, end_year, students,
                             graduates, dropout])

    def add_student_to_classroom(self, student, classroom):
        """Add a new student into an existing classroom in the Classroom
        Register."""
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            # Create a list of entries from the Classroom Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file, delimiter=';')
            # Find an appropriate classroom in the Classroom Register and
            # update its entry index
            row_index = None
            for row in rows:
                if classroom.name in row:
                    row_index = rows.index(row)
            # Use found entry index to update the list of entries
            if row_index is not None:
                entry = rows[row_index]
                classroom_name = entry[0]
                start_year = entry[1]
                end_year = entry[2]
                # Strip strings from redundant characters
                students = entry[3].strip("[]").replace("\'", '').split(', ')
                students = [x for x in students if x]
                graduates = entry[4].strip("[]").replace("\'", '').split(', ')
                graduates = [x for x in graduates if x]
                dropout = entry[5].strip("[]").replace("\'", '').split(', ')
                dropout = [x for x in dropout if x]
                # Create an updated row
                new_row = [classroom_name, start_year, end_year, students,
                           graduates, dropout]
                new_row[3].append(student.fullname)
                # Swap the old row with the updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset the whole Classroom Register
                file.seek(0)
                file.truncate(0)
                # Overwrite the Classroom Register with updated list of entries
                writer.writerows(rows)

    def change_student_status(self, student, action):
        """Change student's status if student has graduated or failed a course.
         In the Classroom Register student's name is moved from 'Students' to
         either 'Graduates' or 'Dropout'."""
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            # Create a list of entries from the Classroom Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file, delimiter=';')
            # Find an appropriate classroom in the Classroom Register and
            # update its entry index
            row_index = None
            for row in rows:
                classroom_name = row[0]
                if classroom_name == student.classroom.name:
                    row_index = rows.index(row)
            # Use found entry index to update the list of entries
            if row_index is not None:
                entry = rows[row_index]
                classroom_name = entry[0]
                start_year = classroom_name.split("-")[0]
                end_year = classroom_name.split("-")[1]
                # Strip redundant characters and remove the student from
                # the list of attending students
                students = entry[3].strip("[]").replace("'", '').split(', ')
                students = [x for x in students if x]
                students.remove(student.fullname)
                # Strip redundant characters and move student's info into
                # an appropriate list
                graduates = entry[4].strip("[]").replace("'", '').split(', ')
                graduates = [x for x in graduates if x]
                dropout = entry[5].strip("[]").replace("'", '').split(', ')
                dropout = [x for x in dropout if x]
                if action == 'Graduate':
                    graduates.append(student.fullname)
                elif action == 'Drop':
                    dropout.append(student.fullname)
                new_row = [classroom_name, start_year, end_year, students,
                           graduates, dropout]
                # Swap the old row with the updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset the whole Classroom Register
                file.seek(0)
                file.truncate(0)
                # Overwrite the Classroom Register with updated list of entries
                writer.writerows(rows)


class StudentRegister(Register):
    """
    A child class of class Register representing the Student Register.

    Attributes:
    -------------
    name : str
        The name of the register
    file : str
        The name of the file containing the register, overrides parent class

    Methods:
    -------------
    is_student_in_register(student) \n
    is_student_attending_course(student, course) \n
    extract_student_info(student, info) \n
    new_student(*args) \n
    update_student_info(student, course=None, grade=None)
    """

    def __init__(self):
        super().__init__()
        self.file = 'students.csv'

    def is_student_in_register(self, student):
        """Check if a student is in the Student Register."""
        first_name = student.split(' ')[0]
        last_name = student.split(' ')[1]
        rows = self.read_rows_in_register()
        for row in rows:
            if last_name in row.get('Last name'):
                if first_name in row.get('First name'):
                    return True
                else:
                    continue

    def is_student_attending_course(self, student, course):
        """Check if a student attends a specified course."""
        first_name = student.split(' ')[0]
        last_name = student.split(' ')[1]
        rows = self.read_rows_in_register()
        for row in rows:
            if last_name in row.get('Last name'):
                if first_name in row.get('First name'):
                    courses = row.get('Courses')
                    courses = courses.split('}, {')
                    courses_list = []
                    # Strip strings from redundant characters
                    for item in courses:
                        item = item.replace("[", "").replace("]", "")\
                                   .replace("\'", "").strip("{}")
                        key = item.split(": ")[0]
                        value = item.split(": ")[1].split(", ")
                        value = [] if value[0] == '' else value
                        new_tuple = (key, value)
                        courses_list.append(new_tuple)
                    courses = dict(tup for tup in courses_list)
                    if course in courses.keys():
                        return True
                    else:
                        continue

    def extract_student_info(self, student, info):
        """Extract a specified kind of information from the Student
        Register."""
        fieldnames = ['First name', 'Last name', 'Date of birth',
                      'Classroom', 'Courses', 'Status']
        searched_index = fieldnames.index(info)
        first_name = student.split(' ')[0]
        last_name = student.split(' ')[1]
        rows = self.read_rows_in_register()
        for row in rows:
            if last_name in row.get('Last name'):
                if first_name in row.get('First name'):
                    searched_info = row.get(fieldnames[searched_index])
                    # If the searched information is 'Courses' reformat strings
                    # and return it as a list of dictionaries
                    if searched_index == 4:
                        courses_list = []
                        searched_info = searched_info.split("}, {")
                        for item in searched_info:
                            item = item.replace("[", "").replace("]", "") \
                                       .replace("\'", "").strip("{}")
                            key = item.split(": ")[0]
                            value = item.split(": ")[1].split(", ")
                            value = [] if value[0] == '' else value
                            new_tuple = (key, value)
                            courses_list.append(new_tuple)
                        searched_info = []
                        for tup in courses_list:
                            new_dict = {tup[0]: tup[1]}
                            searched_info.append(new_dict)
                    return searched_info
                else:
                    continue

    def new_student(self, *args):
        """Add a new student into the Student Register."""
        #  Create a new Student instance
        new_student_item = Student(*args)
        # Write new student's data into the Student Register
        with open(self.file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            first_name = new_student_item.first_name
            last_name = new_student_item.last_name
            date_of_birth = new_student_item.birth_date
            classroom = new_student_item.classroom
            courses = new_student_item.courses
            status = new_student_item.status
            writer.writerow([first_name, last_name, date_of_birth, classroom,
                             courses, status])
        print(f'New student {new_student_item.fullname} has been added to the '
              f'Register')

    def update_student_info(self, student, course=None, grade=None):
        """Update information about a student in the Student Register. This
        method updates information if the student gets a grade, starts a new
        course or changes their status to 'Graduate' or 'Inactive'."""
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            # Create a list of entries from the Student Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file, delimiter=';')
            # Find the student's name in the Student Register and update the
            # entry index
            row_index = None
            for row in rows:
                if student.last_name in row[1]:
                    if student.first_name in row[0]:
                        row_index = rows.index(row)
            # Use found entry index to update the list of entries
            if row_index is not None:
                entry = rows[row_index]
                first_name = entry[0]
                last_name = entry[1]
                date_of_birth = entry[2]
                classroom = entry[3]
                courses = entry[4]
                courses = courses.split('}, {')
                status = student.status
                courses_list = []
                new_row = []
                # Strip strings from redundant characters
                for item in courses:
                    item = item.replace("[", "").replace("]", "")\
                               .replace("\'", "").strip("{}")
                    key = item.split(": ")[0]
                    value = item.split(": ")[1].split(", ")
                    value = [] if value[0] == '' else value
                    # Update student's grades for a specific course if provided
                    # with a new grade
                    if grade:
                        if key == course.course_name:
                            value.append(grade)
                    new_tuple = (key, value)
                    courses_list.append(new_tuple)
                # Update student's courses list if they started a new course
                if not grade:
                    if student and course:
                        new_course = (course.course_name, [])
                        courses_list.append(new_course)
                courses = []
                for tup in courses_list:
                    new_dict = {tup[0]: tup[1]}
                    courses.append(new_dict)
                # Create an updated row
                updated_row = [first_name, last_name, date_of_birth,
                               classroom, courses, status]
                for info in updated_row:
                    new_row.append(info)
                # Swap the old row with the updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset the whole Student Register
                file.seek(0)
                file.truncate(0)
                # Overwrite the Student Register with updated list of entries
                writer.writerows(rows)


class CourseRegister(Register):
    """
    A child class of class Register representing the Course Register.

    Attributes:
    -------------
    name : str
        The name of the register
    file : str
        The name of the file containing the register, overrides parent class

    Methods:
    -------------
    is_course_in_register(course) \n
    extract_course_info(course, info) \n
    new_course(course) \n
    add_student_to_course(student, course) \n
    change_student_status(course, student, action)
    """

    def __init__(self):
        super().__init__()
        self.file = 'courses.csv'

    def is_course_in_register(self, course):
        """Check if a course is in the Course Register."""
        rows = self.read_rows_in_register()
        for row in rows:
            if course in row.get('Course name'):
                course_name = row.get('Course name')
                grade_number = row.get('Grades to pass')
                # Strip strings from redundant characters
                students = row.get('Students').strip('[]')
                students = students.replace("\'", "").split(', ') \
                    if students else []
                graduates = row.get('Graduates').strip('[]')
                graduates = graduates.replace("\'", "").split(', ') \
                    if graduates else []
                dropout = row.get('Dropout').strip('[]')
                dropout = dropout.replace("\'", "").split(', ') \
                    if dropout else []
                course = Course(course_name, grade_number, students,
                                graduates, dropout)
                return course
            else:
                continue

    def extract_course_info(self, course, info):
        """Extract a specified kind of information from the Course Register."""
        fieldnames = ['Course name', 'Grades to pass', 'Students', 'Graduates',
                      'Dropout']
        searched_index = fieldnames.index(info)
        rows = self.read_rows_in_register()
        for row in rows:
            if course in row.get('Course name'):
                searched_info = row.get(fieldnames[searched_index])
                if searched_index in [2, 3, 4]:
                    searched_info = [] if searched_info == '[]' else \
                        searched_info.strip('[]').replace('\'', '').split(', ')
                return searched_info
            else:
                continue

    def new_course(self, course):
        """Add a new course into the Course Register."""
        with open(self.file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            course_name = course.course_name
            grades_number = course.grades_number
            students = course.attending_students
            graduates = course.graduates
            dropout = course.dropouts
            writer.writerow([course_name, grades_number, students,
                             graduates, dropout])

    def add_student_to_course(self, student, course):
        """Add a new student to a specified course in the Course Register."""
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            # Create a list of entries from the Course Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file, delimiter=';')
            # Find an appropriate course in the Course Register and update its
            # entry index
            row_index = None
            for row in rows:
                course_name = row[0]
                if course_name == course:
                    row_index = rows.index(row)
                else:
                    continue
            # Use found entry index to update the list of entries
            if row_index is not None:
                entry = rows[row_index]
                course_name = entry[0]
                grades_number = entry[1]
                # Strip strings from redundant characters
                students = entry[2].strip("[]").replace("\'", '').split(', ')
                students = [x for x in students if x]
                graduates = entry[3].strip("[]").replace("\'", '').split(', ')
                graduates = [x for x in graduates if x]
                dropout = entry[4].strip("[]").replace("\'", '').split(', ')
                dropout = [x for x in dropout if x]
                # Create an updated row
                new_row = [course_name, grades_number, students, graduates,
                           dropout]
                new_row[2].append(student.fullname)
                # Swap the old row with the updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset the whole Course Register
                file.seek(0)
                file.truncate(0)
                # Overwrite the Course Register with updated list of entries
                writer.writerows(rows)

    def change_student_status(self, course, student, action):
        """Change student's status if student has passed or failed a course.
        In the Course Register student's name is moved from 'Students' to
        either 'Graduates' or 'Dropout'."""
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            # Create a list of entries from Course Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file, delimiter=';')
            # Find appropriate course in Course Register and update its
            # entry index
            row_index = None
            for row in rows:
                course_name = row[0]
                if course_name == course.course_name:
                    row_index = rows.index(row)
            # Use found entry index to update entry
            if row_index is not None:
                entry = rows[row_index]
                course_name = entry[0]
                grades_number = entry[1]
                # Strip redundant characters and remove student from attending
                # students
                students = entry[2].strip("[]").replace("'", '').split(', ')
                students = [x for x in students if x]
                students.remove(student.fullname)
                # Strip redundant characters and move student's info into
                # appropriate list
                graduates = entry[3].strip("[]").replace("'", '').split(', ')
                graduates = [x for x in graduates if x]
                dropout = entry[4].strip("[]").replace("'", '').split(', ')
                dropout = [x for x in dropout if x]
                if action == 'Graduate':
                    graduates.append(student.fullname)
                elif action == 'Drop':
                    dropout.append(student.fullname)
                new_row = [course_name, grades_number, students, graduates,
                           dropout]
                # Swap old row with updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset whole Course Register
                file.seek(0)
                file.truncate(0)
                # Overwrite Course Register with updated list of entries
                writer.writerows(rows)


class Classroom:
    """
    A class representing a classroom.

    Attributes:
    -------------
    start_year : int
        A starting year for the classroom
    end_year : int
        A graduation year for the classroom
    name : str
        The name of a classroom represented as 'start_year-end_year'
    years_num : int
        The number of years between end_year and start_year
    student_list : list
        The list of active students' names assigned to the classroom
    graduates: list
        The list of students who has graduated the classroom
    dropout_list: list
        The list of students who has dropped out the classroom

    Methods:
    -------------
    add_student_to_classroom(student) \n
    graduate_student(student) \n
    drop_out_student(student)
    """

    def __init__(self, start_year, end_year, students=None, graduates=None,
                 dropout=None):
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        self.name = f'{start_year}-{end_year}'
        self.years_num = int(end_year) - int(start_year)
        self.student_list = [] if not students else students
        self.graduates = [] if not graduates else graduates
        self.dropout_list = [] if not dropout else dropout

    def __repr__(self):
        return self.name

    def add_student_to_classroom(self, student):
        """Add a student into Classroom instance."""
        self.student_list.append(student)
        return self.student_list

    def graduate_student(self, student):
        """Move a student to Classroom instance's graduates list."""
        try:
            self.student_list.remove(student.fullname)
            self.graduates.append(student.fullname)
        except ValueError:
            print(f'{student} not on student list')

    def drop_out_student(self, student):
        """Move a student to Classroom instance's dropout list."""
        try:
            self.student_list.remove(student.fullname)
            self.dropout_list.append(student.fullname)
        except ValueError:
            print(f'{student} not on student list')


class Student:
    """
    A class representing a student.

    Attributes:
    -------------
    first_name : str
        Student's first name
    last_name : str
        Student's last name
    fullname : str
        A string containing student's first and last name
    birth_date = datetime.date
        Student's date of birth
    classroom : Classroom
        Student's assigned classroom
    status : str
        Student's status - Active, Inactive, Graduate
    class_register : ClassroomRegister
        An instance of ClassroomRegister
    course_register : CourseRegister
        An instance of CourseRegister
    student_register : StudentRegister
        An instance of StudentRegister
    courses : list
        A list of student's courses represented as dictionaries of courses'
        names and lists of grades

    Methods:
    -------------
    add_to_course(course) \n
    get_grade(course, grade) \n
    calc_final_grade(grades) \n
    check_passed_courses(courses) \n
    graduate \n
    drop_out
    """

    def __init__(self, first_name, last_name, birth_date, classroom, course,
                 class_register, course_register, student_register, status):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.fullname = f'{first_name} {last_name}'
        # Convert birth_date (yyyy-mm-dd) to datetime Date class
        date = birth_date.split('-')
        self.birth_date = datetime.date(int(date[0]), int(date[1]),
                                        int(date[2]))
        self.classroom = classroom
        self.status = status if status else 'Active'
        self.class_register = class_register
        self.course_register = course_register
        self.student_register = student_register
        # Check if a student is already in the Student Register
        check_if_registered = \
            self.student_register.is_student_in_register(f'{self.first_name} '
                                                         f'{self.last_name}')
        # If yes, create a list of their courses depending on the number of
        # their courses
        if check_if_registered:
            self.courses = []
            if len(course) > 1:
                for course_item in course:
                    course_name = [x for x in course_item.keys()][0]
                    grades = course_item.get(course_name)
                    self.courses.append({course_name: [grade for grade in
                                                       grades]})
            else:
                course_name = [x for x in course[0].keys()][0]
                grades = [x for x in course[0].values()][0]
                self.courses.append({course_name: grades})
        # If the student is not in the Register create a list of courses with
        # the prompted course as the first and an empty list of grades
        else:
            self.courses = [{course: []}]
            # Automatically add the student to prompted classroom instance
            classroom.add_student_to_classroom(self)
            # Automatically assign the student to a classroom in the Classroom
            # Register
            class_register.add_student_to_classroom(self, classroom)
            # Automatically add the student to the prompted course instance
            course.add_student_to_course(self)
            # Automatically assign the student to a course in the Course
            # Register
            course_register.add_student_to_course(self, course.course_name)

    def __repr__(self):
        return self.fullname

    def add_to_course(self, course):
        """Add a course to Student instance and update Student and Course
        Registers."""
        course_entry = {course.course_name: []}
        self.courses.append(course_entry)
        self.student_register.update_student_info(self, course)
        course.attending_students.append(self)
        self.course_register.add_student_to_course(self, course.course_name)
        print(f'Student {self.fullname} has been added to '
              f'{course.course_name} course')

    def get_grade(self, course, grade):
        """Assign a grade to a specified course of Student instance. If
        conditions for passing the course are met, calculate final grade for
        the course and update the registers, else just update the registers."""
        # For a dictionary in the courses' list
        for course_dict in self.courses:
            # if the prompted course is in dictionary's keys
            if course.course_name in course_dict.keys():
                # append the prompted grade to the values in the dictionary
                course_dict.get(course.course_name).append(grade)
                # Check the number of grades already received
                if len(course_dict.get(course.course_name)) < \
                        course.grades_number:
                    print(f'Student {self} received a {grade} in {course}')
                # If the number of grades is equal to the maximum number of
                # grades for the course, calculate student's final grade for
                # the course
                elif len(course_dict.get(course.course_name)) == \
                        course.grades_number:
                    final_grade = \
                        self.calc_final_grade(course_dict
                                              .get(course.course_name))
                    # If the final grade is 3 or higher, execute pass_course
                    # and move the student to graduates' list for the course in
                    # the Course Register
                    if final_grade >= 3:
                        course.pass_course(self, final_grade)
                        self.course_register\
                            .change_student_status(course, self,
                                                   action='Graduate')
                        print(f'Student {self} received a {grade} in {course}')
                        print(f'Student {self} has passed {course} with grade '
                              f'{final_grade}')
                    # If the final grade is below 3, execute drop_out_student
                    # and move the student to dropouts' list for the course in
                    # the Course Register
                    else:
                        print(f'Student {self} received a {grade} in {course}')
                        course.drop_out_student(self)
                        self.course_register\
                            .change_student_status(course, self,
                                                   action='Drop')
                        print(f'Student {self} has failed {course}')
                        self.drop_out()
                # Prevent from exceeding the number of grades assigned to the
                # course
                else:
                    print(f'Cannot assign grade for student {self} for course'
                          f' {course}')
                    exit()
                self.student_register.update_student_info(self, course=course,
                                                          grade=grade)
        # Check if the student has passed the required number of courses (3) to
        # graduate from their studies
        if self.status != 'Inactive':
            if len(self.courses) == 3:
                course_names = []
                for course in self.courses:
                    course_name = [x for x in course.keys()][0]
                    course_names.append(course_name)
                check = self.check_passed_courses(course_names)
                if check:
                    self.graduate()

    @staticmethod
    def calc_final_grade(grades):
        """Calculate the final grade if the course's graduation conditions are
        met."""
        grades = [int(grade) for grade in grades]
        final_grade = round(sum(grades) / len(grades))
        return final_grade

    def check_passed_courses(self, courses):
        """Check if the student has passed the required number of courses to
        graduate from their studies."""
        counter = 0
        for course in courses:
            graduates = self.course_register.extract_course_info(course,
                                                                 'Graduates')
            if self.fullname in graduates:
                counter += 1
        if counter >= 3:
            return True
        else:
            return False

    def graduate(self):
        """Change a student's status to 'Graduate' in Classroom instance and
        move them to graduates' list in the Classroom Register."""
        self.classroom.graduate_student(self)
        if self.fullname in self.classroom.graduates:
            self.status = 'Graduate'
            self.class_register.change_student_status(self, action='Graduate')
            print(f'{self.fullname} has graduated {self.classroom}. '
                  f'Congratulations!')

    def drop_out(self):
        """Change a student's status to 'Inactive' in Classroom instance and
        move them to dropouts' list in the Classroom Register."""
        self.classroom.drop_out_student(self)
        if self.fullname in self.classroom.dropout_list:
            self.status = 'Inactive'
            self.class_register.change_student_status(self, action='Drop')
            print(f'{self.fullname} has been removed from student list of '
                  f'{self.classroom}')


class Course:
    """
    A class representing a course.

    Attributes:
    -------------
    course_name : str
        The name of the course
    grades_number : int
        The number of grades required to pass the course
    attending_students : list
        The list of students attending the course
    graduates : list
        The list of students who graduated from the course
    dropouts : list
        The list of students who failed to pass the course

    Methods:
    -------------
    add_student_to_course(student)
    pass_course(student, final_grade)
    drop_out_student(student)
    """

    def __init__(self, course_name, grades_number, students=None,
                 graduates=None, dropout=None):
        self.course_name = course_name
        self.grades_number = int(grades_number)
        self.attending_students = [] if not students else students
        self.graduates = [] if not graduates else graduates
        self.dropouts = [] if not dropout else dropout

    def __repr__(self):
        return self.course_name

    def add_student_to_course(self, student):
        """Add a student to Course instance."""
        self.attending_students.append(student.fullname)
        return self.attending_students

    def pass_course(self, student, final_grade):
        """Remove a student from students' list and then append them to
        graduates' list of Course instance."""
        for student_item in self.attending_students:
            if student_item == student.fullname:
                self.attending_students.remove(student_item)
        self.graduates.append({student.fullname: final_grade})

    def drop_out_student(self, student):
        """Remove a student from students' list and then append them to
        dropouts' list of Course instance."""
        for student_item in self.attending_students:
            if student_item == student.fullname:
                self.attending_students.remove(student_item)
        self.dropouts.append(student.fullname)


def new_classroom_func(class_reg, start_year, end_year):
    classroom_name = start_year + '-' + end_year

    # Check if the prompted classroom exists in the register
    check = class_reg.is_classroom_in_register(classroom_name)
    # Add a new classroom into the register if it has not been registered
    if check:
        print(f'{classroom_name} already exists')
    else:
        new_classroom = Classroom(start_year, end_year)
        class_reg.new_classroom(new_classroom)
        print(f'{new_classroom} has been added to register')


def new_student_func(class_reg, course_reg, student_reg, firstname, lastname,
                     birthdate, classroom, course):
    fullname = f'{firstname} {lastname}'
    # Test if the prompted classroom exists in the register
    assigned_classroom = class_reg.is_classroom_in_register(classroom)
    # Exit creating student if the assigned classroom does not exist
    if not assigned_classroom:
        print(f'Classroom {classroom} does not exist. Create a new '
              f'classroom first!')
        exit()
    # Test if the prompted course exists in the register
    first_course = course_reg.is_course_in_register(course)
    # Exit creating student if the assigned course does not exist
    if not first_course:
        print(f'Course {course} does not exist. Create new course '
              f'first!')
        exit()

    # Check if the student is already in the Student Register
    check_student = student_reg.is_student_in_register(fullname)
    # If the student is registered exit program, else begin creation of a
    # new student in the Student Register
    if check_student:
        print(f'Student {fullname} is already registered!')
        exit()
    else:
        student_reg.new_student(firstname, lastname, birthdate, classroom,
                                course, class_reg, course_reg, student_reg)


def new_course_func(course_reg, course_name, grades_number):
    # Check if the prompted course exists in the register
    check = course_reg.is_course_in_register(course_name)
    # Add a new course into the register if it has not been registered
    if check:
        print(f'{course_name} already exists')
    else:
        new_course = Course(course_name, grades_number)
        course_reg.new_course(new_course)
        print(f'{new_course} has been added to register')


def append_to_course_func(class_reg, course_reg, student_reg, firstname,
                          lastname, course_name):
    student_name = f'{firstname} {lastname}'
    # Check if the prompted student exists in the register
    is_student = student_reg.is_student_in_register(student_name)
    # Check if the prompted course exists in the register
    is_course = course_reg.is_course_in_register(course_name)
    # If both conditions are met, check if the student has been already
    # attending the course
    if is_student and is_course:
        is_student_in_course = \
            student_reg.is_student_attending_course(student_name, course_name)
        # Prevent from appending the student to the course that they have
        # been already attending by exiting the program
        if is_student_in_course:
            print(f'Student {student_name} is already attending '
                  f'{course_name}')
            exit()
        # Otherwise, create a Student instance based on the data from the
        # Student Register
        else:
            date_of_birth = \
                student_reg.extract_student_info(student_name,
                                                 'Date of birth')
            classroom_name = student_reg.extract_student_info(student_name,
                                                              'Classroom')
            classroom = class_reg.is_classroom_in_register(classroom_name)
            courses = student_reg.extract_student_info(student_name,
                                                       'Courses')
            student_object = Student(firstname, lastname, date_of_birth,
                                     classroom, courses, class_reg, course_reg,
                                     student_reg, status='Active')
            # Create a Course instance based on the data from the Course
            # Register
            grades_number = \
                course_reg.extract_course_info(course_name, 'Grades to pass')
            students = course_reg.extract_course_info(course_name, 'Students')
            graduates = course_reg.extract_course_info(course_name,
                                                       'Graduates')
            dropout = course_reg.extract_course_info(course_name, 'Dropout')
            course_object = Course(course_name, grades_number, students,
                                   graduates, dropout)
            student_object.add_to_course(course_object)


def give_grade_func(class_reg, course_reg, student_reg, firstname, lastname,
                    course_name, grade):
    student_name = f'{firstname} {lastname}'
    # Check if the course exists and exit program if it does not
    check_course = course_reg.is_course_in_register(course_name)
    if not check_course:
        print(f'Course {course_name} does not exist. Create a new '
              f'course first!')
        exit()

    # Check if the student is registered and exit program if they do not
    check_student = student_reg.is_student_in_register(student_name)
    if not check_student:
        print(f'Student {student_name} has not been registered.')
        exit()

    # Check if the student attends the course and exit program if they do
    # not
    check_student_in_course = \
        student_reg.is_student_attending_course(student_name, course_name)
    if check_student_in_course:
        # Create a Student instance based on the data from the Student
        # Register
        date_of_birth = student_reg.extract_student_info(student_name,
                                                         'Date of birth')
        classroom_name = student_reg.extract_student_info(student_name,
                                                          'Classroom')
        classroom = class_reg.is_classroom_in_register(classroom_name)
        courses = student_reg.extract_student_info(student_name, 'Courses')
        status = student_reg.extract_student_info(student_name, 'Status')
        # Prevent students with status 'Inactive' or 'Graduate' from
        # getting a grade by exiting thr program
        if status == 'Inactive' or status == 'Graduate':
            print(f'{student_name} is not on active students list for '
                  f'{course_name}')
            exit()
        student_object = Student(firstname, lastname, date_of_birth, classroom,
                                 courses, class_reg, course_reg, student_reg,
                                 status)
        # Create a Course instance based on the data from the Course
        # Register
        grades_number = course_reg.extract_course_info(course_name,
                                                       'Grades to pass')
        students = course_reg.extract_course_info(course_name, 'Students')
        graduates = course_reg.extract_course_info(course_name, 'Graduates')
        dropout = course_reg.extract_course_info(course_name, 'Dropout')
        course_object = Course(course_name, grades_number, students,
                               graduates, dropout)
        # Execute Student instance's get_grade method
        student_object.get_grade(course_object, grade)
    else:
        print(f'{student_name} does not attend {course_name}')
        exit()


def main():
    """The main function based on the argument parser."""

    class_reg = ClassroomRegister()
    student_reg = StudentRegister()
    course_reg = CourseRegister()

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    print_register = subparser.add_parser('print_register')
    print_register.add_argument('register', choices=['classrooms', 'students',
                                                     'courses'],
                                help='Print a specified register: Classroom '
                                     'Register, Student Register, Course '
                                     'Register')

    new_classroom = subparser.add_parser('new_classroom',
                                         help='Register a new classroom')
    new_classroom.add_argument('start_year', help='Starting year for the '
                                                  'classroom: yyyy')
    new_classroom.add_argument('end_year', help='Predicted graduation year for'
                                                ' the classroom: yyyy')

    new_student = subparser.add_parser('new_student',
                                       help='Register a new student')
    new_student.add_argument('firstname', help="Student's first name")
    new_student.add_argument('lastname', help="Student's last name")
    new_student.add_argument('birthdate', help="Student's date of birth: "
                                               "yyyy-mm-dd")
    new_student.add_argument('classroom', help="Student's assigned classroom "
                                               "name: yyyy-yyyy")
    new_student.add_argument('course', help="Student's assigned first course")

    new_course = subparser.add_parser('new_course',
                                      help='Register a new course')
    new_course.add_argument('course_name', help='The name of the course')
    new_course.add_argument('grades_number', help='Number of grades required '
                                                  'to pass the course: int')

    append_to_course = subparser.add_parser('append_to_course',
                                            help='Add a registered student to '
                                                 'another existing course')
    append_to_course.add_argument('firstname', help="Student's first name")
    append_to_course.add_argument('lastname', help="Student's last name")
    append_to_course.add_argument('course_name',
                                  help='The name of a registered course that '
                                       'the student should be appended to')

    give_grade = subparser.add_parser('give_grade',
                                      help='Give a grade to a registered '
                                           'student')
    give_grade.add_argument('firstname', help="Student's first name")
    give_grade.add_argument('lastname', help="Student's last name")
    give_grade.add_argument('course_name',
                            help='The name of a registered course that the '
                                 'student should be graded for')
    give_grade.add_argument('grade', choices=range(2, 6),
                            help='Available grades: 2, 3, 4, 5')

    args = parser.parse_args()

    if args.command == 'print_register':
        if args.reg_name == 'classrooms':
            class_reg.print_register()
        elif args.reg_name == 'students':
            student_reg.print_register()
        elif args.reg_name == 'courses':
            course_reg.print_register()
        else:
            print('Invalid register, please choose from "classrooms", '
                  '"students", "courses"')

    elif args.command == 'new_classroom':
        new_classroom_func(class_reg, args.start_year, args.end_year)

    elif args.command == 'new_student':
        new_student_func(class_reg, course_reg, student_reg, args.firstname,
                         args.lastname, args.birthdate, args.classroom,
                         args.course)

    elif args.command == 'new_course':
        new_course_func(course_reg, args.course_name, args.grades_number)

    elif args.command == 'append_to_course':
        append_to_course_func(class_reg, course_reg, student_reg,
                              args.firstname, args.lastname, args.course_name)

    elif args.command == 'give_grade':
        give_grade_func(class_reg, course_reg, student_reg, args.firstname,
                        args.lastname, args.course_name, args.grade)


if __name__ == '__main__':
    main()
