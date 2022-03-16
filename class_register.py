#!/usr/bin/python3

# Dictionary:
# Classroom Register = 'classrooms.csv'
# Student Register = 'students.csv'
# Course Register = 'courses.csv'

import datetime
import csv
import argparse


class Register:

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

    def __init__(self):
        super().__init__()
        self.file = 'classrooms.csv'

    def is_classroom_in_register(self, classroom):
        """Check if a classroom is in Classroom Register."""
        rows = self.read_rows_in_register()
        for row in rows:
            if classroom in row.get('Class name'):
                start_year = row.get('Start year')
                end_year = row.get('End year')
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
        """Extract specific kind of information from Classroom Register."""
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
        """Add a new classroom into Classroom Register."""
        with open(self.file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            classroom_name = classroom.name
            start_year = classroom.start_year
            end_year = classroom.end_year
            students = classroom.student_list
            graduates = classroom.graduates
            dropout = classroom.drop_out_list
            writer.writerow([classroom_name, start_year, end_year, students,
                             graduates, dropout])

    def add_student_to_classroom(self, student, classroom):
        """Add a new student into existing classroom in Classroom Register."""
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            # Create a list of entries from Classroom Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file, delimiter=';')
            # Find appropriate classroom in Classroom Register and update its
            # entry index
            row_index = None
            for row in rows:
                if classroom.name in row:
                    row_index = rows.index(row)
            # Use found entry index to update list of entries
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
                # Create updated row
                new_row = [classroom_name, start_year, end_year, students,
                           graduates, dropout]
                new_row[3].append(student.fullname)
                # Swap old row with updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset whole Classroom Register
                file.seek(0)
                file.truncate(0)
                # Overwrite Classroom Register with updated list of entries
                writer.writerows(rows)

    def move_student_to_graduates(self, student):
        pass

    def move_student_to_dropouts(self, student):
        pass


class StudentRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'students.csv'
        self.selected_classroom = None

    def is_student_in_register(self, student):
        """Check if a student is in Student Register."""
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
        """Check if a student attends a specific course."""
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
        """Extract specific kind of information from Student Register."""
        fieldnames = ['First name', 'Last name', 'Date of birth',
                      'Classroom', 'Courses']
        searched_index = fieldnames.index(info)
        first_name = student.split(' ')[0]
        last_name = student.split(' ')[1]
        rows = self.read_rows_in_register()
        for row in rows:
            if last_name in row.get('Last name'):
                if first_name in row.get('First name'):
                    searched_info = row.get(fieldnames[searched_index])
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
                        searched_info = dict(tup for tup in courses_list)
                    return searched_info
                else:
                    continue

    def new_student(self, *args):
        """Add a new student into Student Register."""
        #  Create new Student instance
        new_student_item = Student(*args)
        # Write new student data into Student Register
        with open(self.file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            first_name = new_student_item.first_name
            last_name = new_student_item.last_name
            date_of_birth = new_student_item.birth_date
            classroom = new_student_item.classroom
            courses = new_student_item.courses
            writer.writerow([first_name, last_name, date_of_birth, classroom,
                             courses])
        print(f'New student {new_student_item.fullname} has been added to the '
              f'Register')

    def move_student_to_graduates(self, student):
        pass

    def move_student_to_dropouts(self, student):
        pass

    def update_student_info(self, student, course=None, grade=None):
        """Update information about student in the Student Register"""
        # Update student's grades for a specific course
        if course and grade:
            with open(self.file, 'r+', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                # Create a list of entries from Student Register
                rows = []
                for row in reader:
                    rows.append(row)
                writer = csv.writer(file, delimiter=';')
                row_index = None
                for row in rows:
                    if student.last_name in row[1]:
                        if student.first_name in row[0]:
                            row_index = rows.index(row)
                # Use found entry index to update entry
                if row_index is not None:
                    entry = rows[row_index]
                    first_name = entry[0]
                    last_name = entry[1]
                    date_of_birth = entry[2]
                    classroom = entry[3]
                    courses = entry[4]
                    courses = courses.split('}, {')
                    courses_list = []
                    # Strip strings from redundant characters
                    for item in courses:
                        item = item.replace("[", "").replace("]", "")\
                                   .replace("\'", "").strip("{}")
                        key = item.split(": ")[0]
                        value = item.split(": ")[1].split(", ")
                        value = [] if value[0] == '' else value
                        value.append(grade)
                        new_tuple = (key, value)
                        courses_list.append(new_tuple)
                    courses = dict(tup for tup in courses_list)
                    # Create updated row
                    new_row = [first_name, last_name, date_of_birth,
                               classroom, courses]
                    # Swap old row with updated one
                    rows.remove(rows[row_index])
                    rows.insert(row_index, new_row)
                    # Reset whole Student Register
                    file.seek(0)
                    file.truncate(0)
                    # Overwrite Student Register with updated list of entries
                    writer.writerows(rows)


class CourseRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'courses.csv'

    def is_course_in_register(self, course):
        """Check if a course is in Course Register."""
        rows = self.read_rows_in_register()
        for row in rows:
            if course in row.get('Course name'):
                course_name = row.get('Course name')
                grade_number = row.get('Grades to pass')
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
        """Extract specific kind of information from Course Register."""
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
        """Add a new course into Course Register."""
        with open(self.file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            course_name = course.course_name
            grades_number = course.grades_number
            students = course.attending_students
            graduates = course.graduates
            dropout = course.drop_outs
            writer.writerow([course_name, grades_number, students,
                             graduates, dropout])

    def add_student_to_course(self, student, course):
        """Add a new student to a specific course in Course Register."""
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
                for course_item in course:
                    key_from_course_attr = str(course_item.keys())
                    if course_name in key_from_course_attr:
                        row_index = rows.index(row)
                    else:
                        continue
            # Use found entry index to update entry
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
                # Create updated row
                new_row = [course_name, grades_number, students, graduates,
                           dropout]
                new_row[2].append(student.fullname)
                # Swap old row with updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset whole Course Register
                file.seek(0)
                file.truncate(0)
                # Overwrite Course Register with updated list of entries
                writer.writerows(rows)

    def move_student_to_graduates(self, course, student):
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
                # Strip redundant characters and update graduates' list with
                # student's info
                graduates = entry[3].strip("[]").replace("'", '').split(', ')
                graduates = [x for x in graduates if x]
                graduates.append(student.fullname)
                dropout = entry[4].strip("[]").replace("'", '').split(', ')
                dropout = [x for x in dropout if x]
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

    def move_student_to_dropouts(self, course, student):
        pass


class Classroom:

    def __init__(self, start_year, end_year, students=None, graduates=None,
                 dropout=None):
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        self.name = f'{start_year}-{end_year}'
        self.years_num = int(end_year) - int(start_year)
        self.student_list = [] if not students else students
        self.drop_out_list = [] if not dropout else dropout
        self.graduates = [] if not graduates else graduates

    def __repr__(self):
        return self.name

    def add_student_to_classroom(self, student):
        """Add a student into Classroom instance."""
        self.student_list.append(student)
        return self.student_list

    def drop_out_student(self, student):
        """Remove a student from Classroom instance."""
        self.student_list.remove(student)
        self.drop_out_list.append(student)
        return self.student_list, self.drop_out_list

    def _graduate_student(self, student):
        try:
            self.student_list.remove(student)
            self.graduates.append(student)
            return self.student_list, self.graduates
        except ValueError:
            print(f'{student} not on student list')


class Student:

    def __init__(self, first_name, last_name, birth_date, classroom, course,
                 class_register, course_register, student_register):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.fullname = f'{first_name} {last_name}'
        # Convert birth_date (yyyy-mm-dd) to datetime Date class
        date = birth_date.split('-')
        self.birth_date = datetime.date(int(date[0]), int(date[1]),
                                        int(date[2]))
        self.classroom = classroom
        self.status = 'Active'
        self.class_register = class_register
        self.course_register = course_register
        self.student_register = student_register
        check_if_registered = \
            self.student_register.is_student_in_register(f'{self.first_name} '
                                                         f'{self.last_name}')
        if check_if_registered:
            self.courses = []
            if len(course) > 1:
                for course_item in course:
                    course_name = course_item[0]
                    grades = course_item[1]
                    self.courses.append({course_name: grades})
            else:
                course_name = [x for x in course.keys()][0]
                grades = [x for x in course.values()][0]
                self.courses.append({course_name: grades})
        else:
            self.courses = [{course: []}]
            # automatically add student to prompted classroom
            classroom.add_student_to_classroom(self)
            # automatically assign student to classroom in Classroom Register
            class_register.add_student_to_classroom(self, classroom)
            # automatically add student to prompted course
            course.add_student_to_course(self)
            # automatically assign student to course in Course Register
            course_register.add_student_to_course(self, self.courses)

    def __repr__(self):
        return self.fullname

    def add_to_course(self, course):
        """Add a course to Student instance."""
        self.courses.append({course: []})
        course.attending_students.append(self)

    def get_grade(self, course, grade):
        """Assign a grade to a specific course of Student instance. If
        conditions for passing the course are met, calculate final grade for
        the course and update registers, else just update registers."""
        # for item in course list
        for course_item in self.courses:
            # if the course is in keys
            if course.course_name in course_item.keys():
                # append grade to the values in course dictionary
                course_item.get(course.course_name).append(grade)
                # Check the number of grades already received
                if len(course_item.get(course.course_name)) < \
                        course.grades_number:
                    print(f'Student {self} received a {grade} in {course}')
                elif len(course_item.get(course.course_name)) == \
                        course.grades_number:
                    final_grade = \
                        self.calc_final_grade(course_item
                                              .get(course.course_name))
                    if final_grade >= 3:
                        course.pass_course(self, final_grade)
                        # Move student to graduates for the course in Course
                        # Register
                        self.course_register.move_student_to_graduates(course,
                                                                       self)
                        print(f'Student {self} received a {grade} in {course}')
                        print(f'Student {self} has passed {course} with grade '
                              f'{final_grade}')
                    else:
                        course.drop_out_student(self)
                        self.drop_out()
                # Prevent from exceeding the number of grades assigned to the
                # course
                else:
                    print(f'Cannot assign grade for student {self} for course'
                          f' {course}')
                    exit()
                self.student_register.update_student_info(self, course=course,
                                                          grade=grade)
        # to do: check if student passed required number of courses to graduate

    @staticmethod
    def calc_final_grade(grades):
        """Calculate the final grade if course graduation conditions are
        met."""
        grades = [int(grade) for grade in grades]
        final_grade = round(sum(grades) / len(grades))
        return final_grade

    def graduate(self):
        self.classroom._graduate_student(self)
        if self in self.classroom.graduates:
            self.status = 'Graduate'
            # to do: update Classroom and Student Register

    def drop_out(self):
        self.status = 'Inactive'
        self.classroom.drop_out_student(self)
        # to do: update Classroom and Student Register


class Course:

    def __init__(self, course_name, grades_number, students=None,
                 graduates=None, dropout=None):
        self.course_name = course_name
        self.attending_students = [] if not students else students
        self.graduates = [] if not graduates else graduates
        self.drop_outs = [] if not dropout else dropout
        self.grades_number = int(grades_number)

    def __repr__(self):
        return self.course_name

    def add_student_to_course(self, student):
        """Add student to Course instance."""
        self.attending_students.append(student)
        return self.attending_students

    def pass_course(self, student, final_grade):
        for student_item in self.attending_students:
            if student_item == student:
                self.attending_students.remove(student)
        self.graduates.append({student: final_grade})
        # to do: update Course Register

    def drop_out_student(self, student):
        pass  # append student into dropout list, update registers


def main():
    class_reg = ClassroomRegister()
    student_reg = StudentRegister()
    course_reg = CourseRegister()

    parser = argparse.ArgumentParser()
    # print Classroom Register
    parser.add_argument('--print_class', action='store_true',
                        help='Print classroom register')
    # print Student Register
    parser.add_argument('--print_students', action='store_true',
                        help='Print student register')
    # print Course Register
    parser.add_argument('--print_courses', action='store_true',
                        help='Print courses register')
    # add new classroom to Classroom Register
    parser.add_argument('--new_classroom', nargs='*',
                        help='Add new classroom, give start year, end year')
    # add new student to Student Register
    parser.add_argument('--new_student', nargs=5,
                        help='Add new student: give first name, last name, '
                             'date of birth yyyy-mm-dd, existing assigned '
                             'classroom, at least one existing course to '
                             'assign')
    # add new course to Course Register
    parser.add_argument('--new_course', nargs='*',
                        help='Add new course, give course name, number of '
                             'grades to pass')
    # give grade to student
    parser.add_argument('--give_grade', nargs='*',
                        help="Give grade to student, give course, grade, "
                             "student's name")

    args = parser.parse_args()

    if args.print_class:
        class_reg.print_register()

    elif args.print_students:
        student_reg.print_register()

    elif args.print_courses:
        course_reg.print_register()

    elif args.new_classroom:
        start_year, end_year = args.new_classroom[0], args.new_classroom[1]
        classroom_name = start_year + '-' + end_year

        # Check if prompted classroom exists in the register
        check = class_reg.is_classroom_in_register(classroom_name)
        # Add a new classroom into the register if it has not been registered
        if check:
            print(f'{classroom_name} already exists')
        else:
            new_classroom = Classroom(start_year, end_year)
            class_reg.new_classroom(new_classroom)
            print(f'{new_classroom} has been added to register')

    elif args.new_student:
        args_ = args.new_student
        first_name, last_name, birthdate = args_[0], args_[1], args_[2]
        fullname = f'{first_name} {last_name}'
        # test if prompted classroom exists in the register
        assigned_classroom = class_reg.is_classroom_in_register(args_[3])
        # exit creating student if assigned classroom does not exist
        if not assigned_classroom:
            print(f'Classroom {args_[3]} does not exist. Create new classroom '
                  f'first!')
            exit()
        # test if prompted course exists in the register
        first_course = course_reg.is_course_in_register(args_[4])
        # exit creating student if assigned course does not exist
        if not first_course:
            print(f'Course {args_[4]} does not exist. Create new course '
                  f'first!')
            exit()

        # Check if student is already in Student Register
        check_student = student_reg.is_student_in_register(fullname)
        # If student is registered exit program, else begin creation of new
        # Student in Student Register
        if check_student:
            print(f'Student {fullname} is already registered!')
            exit()
        else:
            student_reg.new_student(first_name, last_name, birthdate,
                                    assigned_classroom, first_course,
                                    class_reg, course_reg, student_reg)

    elif args.new_course:
        course_name, grades_number = args.new_course[0], args.new_course[1]

        # Check if prompted course exists in the register
        check = course_reg.is_course_in_register(course_name)
        # Add a new course into the register if it has not been registered
        if check:
            print(f'{course_name} already exists')
        else:
            new_course = Course(course_name, grades_number)
            course_reg.new_course(new_course)
            print(f'{new_course} has been added to register')

    elif args.give_grade:
        course_name = args.give_grade[0]
        grade = args.give_grade[1]
        student_name = args.give_grade[2]

        # Check if course exists and exit program if it does not
        check_course = course_reg.is_course_in_register(course_name)
        if not check_course:
            print(f'Course {course_name} does not exist. Create new course'
                  f'first!')
            exit()  # exit program if course does not exist

        # Check if student exists
        check_student = student_reg.is_student_in_register(student_name)
        if not check_student:
            print(f'Student {student_name} does not exist.')
            exit()  # exit program if student does not exist

        # Check if student attends course
        check_student_in_course = \
            student_reg.is_student_attending_course(student_name, course_name)
        if check_student_in_course:
            # Create student object from register data
            first_name = student_name.split(' ')[0]
            last_name = student_name.split(' ')[1]
            date_of_birth = student_reg.extract_student_info(student_name,
                                                             'Date of birth')
            classroom_name = student_reg.extract_student_info(student_name,
                                                              'Classroom')
            classroom = class_reg.is_classroom_in_register(classroom_name)
            courses = student_reg.extract_student_info(student_name, 'Courses')
            student_object = Student(first_name, last_name, date_of_birth,
                                     classroom, courses, class_reg,
                                     course_reg, student_reg)
            # Create course object from register data
            grades_number = course_reg.extract_course_info(course_name,
                                                           'Grades to pass')
            students = course_reg.extract_course_info(course_name, 'Students')
            graduates = course_reg.extract_course_info(course_name,
                                                       'Graduates')
            dropout = course_reg.extract_course_info(course_name, 'Dropout')
            course_object = Course(course_name, grades_number, students,
                                   graduates, dropout)
            student_object.get_grade(course_object, grade)
        else:
            print(f'{student_name} does not attend {course_name}')
            exit()  # exit program if student does not attend course


if __name__ == '__main__':
    main()
