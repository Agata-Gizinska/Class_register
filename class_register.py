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

    def print_register(self):
        with open(self.file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)


class ClassroomRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'classrooms.csv'

    # Check if a classroom is in Classroom Register
    def is_classroom_in_register(self, classroom):
        with open(self.file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = []
            for row in reader:
                rows.append(row)
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

    # Add a new classroom into Classroom Register
    def new_classroom(self, classroom):
        with open(self.file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            classroom_name = classroom.name
            start_year = classroom.start_year
            end_year = classroom.end_year
            students = classroom.student_list
            graduates = classroom.graduates
            dropout = classroom.drop_out_list
            writer.writerow([classroom_name, start_year, end_year, students,
                             graduates, dropout])

    # Add a new student into existing classroom in Classroom Register
    def add_student_to_classroom(self, student, classroom):
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Create a list of entries from Classroom Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file)
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
                students = entry[3].strip("[]").replace("'", '').split(',')
                students = [x for x in students if x]
                graduates = entry[4].strip("[]").replace("'", '').split(',')
                graduates = [x for x in graduates if x]
                dropout = entry[5].strip("[]").replace("'", '').split(',')
                dropout = [x for x in dropout if x]
                new_row = [classroom_name, start_year, end_year, students,
                           graduates, dropout]
                new_row[3].append(student.fullname)
                # swap old row with updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset whole Classroom Register
                file.seek(0)
                file.truncate(0)
                # Overwrite Classroom Register with updated list of entries
                writer.writerows(rows)

    def remove_student_from_classroom(self, student):
        pass


class StudentRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'students.csv'
        self.selected_classroom = None

    # Add a new student into Student Register
    def new_student(self, *args):
        # create new Student instance
        new_student_ = Student(*args)
        # write new student data into Student Register
        with open(self.file, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['First name', 'Last name', 'Date of Birth',
                          'Classroom', 'Courses']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({fieldnames[0]: new_student_.first_name,
                             fieldnames[1]: new_student_.last_name,
                             fieldnames[2]: new_student_.birth_date,
                             fieldnames[3]: new_student_.classroom,
                             fieldnames[4]: new_student_.courses})
        print(f'New student {new_student_.fullname} has been added to the '
              f'Register')

    def move_to_graduates(self, student):
        pass

    def move_to_dropout(self, student):
        pass


class CourseRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'courses.csv'

    # Check if a course is in Course Register
    @staticmethod
    def is_course_in_register(course):
        with open('courses.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = []
            for row in reader:
                rows.append(row)
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

    # Add a new course into Course Register
    def new_course(self, course):
        with open(self.file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            course_name = course.course_name
            grades_number = course.grades_number
            students = course.attending_students
            graduates = course.graduates
            dropout = course.drop_outs
            writer.writerow([course_name, grades_number, students,
                             graduates, dropout])

    # Add a new student to a specific course in Course Register
    def add_student_to_course(self, student, course):
        with open(self.file, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Create a list of entries from Course Register
            rows = []
            for row in reader:
                rows.append(row)
            writer = csv.writer(file)
            # Find appropriate course in Course Register and update its
            # entry index
            row_index = None
            for row in rows:
                course_name = row[0]
                key_from_course_attr = str(course.keys())
                if course_name in key_from_course_attr:
                    row_index = rows.index(row)
            # Use found entry index to update entry
            if row_index is not None:
                entry = rows[row_index]
                course_name = entry[0]
                grades_number = entry[1]
                students = entry[2].strip("[]").replace("'", '').split(',')
                students = [x for x in students if x]
                graduates = entry[3].strip("[]").replace("'", '').split(',')
                graduates = [x for x in graduates if x]
                dropout = entry[4].strip("[]").replace("'", '').split(',')
                dropout = [x for x in dropout if x]
                new_row = [course_name, grades_number, students, graduates,
                           dropout]
                new_row[2].append(student.fullname)
                # swap old row with updated one
                rows.remove(rows[row_index])
                rows.insert(row_index, new_row)
                # Reset whole Course Register
                file.seek(0)
                file.truncate(0)
                # Overwrite Course Register with updated list of entries
                writer.writerows(rows)

    def update_register(self):
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
        return f'Class {self.name}'

    # Add a student into Classroom instance
    def add_student_to_class(self, student):
        self.student_list.append(student)
        return self.student_list

    # Remove a student from Classroom instance
    def drop_out_student(self, student):
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
                 class_register, course_register):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.fullname = f'{first_name} {last_name}'
        # Convert birth_date (yyyy-mm-dd) to datetime Date class
        date = birth_date.split('-')
        self.birth_date = datetime.date(int(date[0]), int(date[1]),
                                        int(date[2]))
        self.classroom = classroom
        self.status = 'Active'
        self.courses = [{course: []}]
        # automatically add student to prompted classroom
        classroom.add_student_to_class(self)
        # automatically assign student to classroom in Classroom Register
        class_register.add_student_to_classroom(self, classroom)
        # automatically add student to prompted course
        course.add_student_to_course(self)
        # automatically assign student to course in Course Register
        course_register.add_student_to_course(self, self.courses[0])

    def __repr__(self):
        return self.fullname

    # Add a course to Student instance
    def add_course(self, course):
        self.courses.append({course: []})
        course.attending_students.append(self)

    # Assign a grade to a specific course of Student instance and check if
    # graduation conditions are met
    def get_grade(self, course, grade):
        for course_ in self.courses:  # for item in course list
            if course in course_.keys():  # if the course is in keys
                course_.get(course).append(grade)  # append grade to values in
                # course dictionary
                if len(course_.get(course)) == course.grades_number:  # check
                    # if student got maximum number of grades for course
                    final_grade = self.calc_final_grade(course_.get(course))
                    if final_grade >= 3:
                        course.pass_course(self, final_grade)
                    else:
                        course.drop_outs.append(self)
                        self.drop_out()
                return self.courses

    # Calculate the final grade if course graduation conditions are met
    @staticmethod
    def calc_final_grade(grades):
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

    # Add student to Course instance
    def add_student_to_course(self, student):
        self.attending_students.append(student)
        return self.attending_students

    # Assign a grade to the specific student in Course instance
    def give_grade(self, student, grade):
        if student in self.attending_students:
            student.get_grade(self, grade)
        else:
            print(f'{student} is not course attendee')

    def pass_course(self, student, grade):
        for student_ in self.attending_students:
            if student_ == student:
                self.attending_students.remove(student)
        self.graduates.append({student: grade})
        return self.attending_students, self.graduates


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
    parser.add_argument('--give_grade', nargs=2,
                        help="Give grade to student, give grade, "
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
            print('Prompted classroom already exists')
        else:
            new_classroom = Classroom(start_year, end_year)
            class_reg.new_classroom(new_classroom)
            print(f'{new_classroom} has been added to register')

    elif args.new_student:
        args_ = args.new_student
        first_name, last_name, birthdate = args_[0], args_[1], args_[2]

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

        # begin creation of new Student in Student Register
        student_reg.new_student(first_name, last_name, birthdate,
                                assigned_classroom, first_course, class_reg,
                                course_reg)

    elif args.new_course:
        course_name, grades_number = args.new_course[0], args.new_course[1]

        # Check if prompted course exists in the register
        check = course_reg.is_course_in_register(course_name)
        # Add a new course into the register if it has not been registered
        if check:
            print('Prompted course already exists')
        else:
            new_course = Course(course_name, grades_number)
            course_reg.new_course(new_course)
            print(f'{new_course} has been added to register')

    elif args.give_grade:
        pass


if __name__ == '__main__':
    main()
