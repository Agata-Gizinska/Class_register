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

    def new_classroom(self):
        pass

    def add_student_to_classroom(self, student, classroom):
        pass

    def remove_student_from_classroom(self, student):
        pass


class StudentRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'students.csv'
        self.selected_classroom = None

    def new_student(self, *args):
        pass

    def move_to_graduates(self, student):
        pass

    def move_to_dropout(self, student):
        pass


class CourseRegister(Register):

    def __init__(self):
        super().__init__()
        self.file = 'courses.csv'

    def new_course(self, name, grades_number):
        pass

    def add_student_to_course(self, student, course):
        pass

    def update_register(self):
        pass


class Classroom:

    def __init__(self, start_year, end_year, students=None, graduates=None,
                 dropout=None):
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        self.name = f'{start_year}-{end_year}'
        self.years_num = int(end_year) - int(start_year)
        self.student_list = students if not None else []
        self.drop_out_list = dropout if not None else []
        self.graduates = graduates if not None else []

    def __repr__(self):
        return f'Class {self.name}'

    # add student to Classroom instance
    def add_student_to_class(self, student):
        self.student_list.append(student)
        return self.student_list

    # add student to Classroom Register
    @staticmethod
    def add_student_to_register(student, register):
        register.add_student_to_classroom(student, student.classroom)

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
        classroom.add_student_to_register(self, class_register)
        # automatically add student to prompted course
        course.add_student_to_course(self)
        # automatically assign student to course in Course Register
        course.add_student_to_register(self, course_register)

    def __repr__(self):
        return self.fullname

    def add_course(self, course):
        self.courses.append({course: []})
        course.attending_students.append(self)
        return self.courses

    def get_grade(self, course, grade):
        for course_ in self.courses:  # for item in course list
            if course in course_.keys():  # if the course is in keys
                course_.get(course).append(grade)  # append grade to values in
                # course dictionary
                if len(course_.get(course)) == course.len_partial:  # check if
                    # student got maximum number of partial grades for course
                    final_grade = self.calc_final_grade(course_.get(course))
                    if final_grade >= 3:
                        course.pass_course(self, final_grade)
                    else:
                        course.drop_outs.append(self)
                        self.drop_out()
                else:
                    pass
                return self.courses
            else:
                pass

    @staticmethod
    def calc_final_grade(grades):
        final_grade = round(sum(grades) / len(grades))
        return final_grade

    def graduate(self):
        self.classroom._graduate_student(self)
        if self in self.classroom.graduates:
            self.status = 'Graduate'
            # to do: update Classroom and Student Register
        else:
            pass

    def drop_out(self):
        self.status = 'Inactive'
        self.classroom.drop_out_student(self)
        # to do: update Classroom and Student Register


class Course:

    def __init__(self, course_name, partial_grades_num, students=None,
                 graduates=None, dropout=None):
        self.course_name = course_name
        self.attending_students = students if not None else []
        self.graduates = graduates if not None else []
        self.drop_outs = dropout if not None else []
        self.len_partial = int(partial_grades_num)

    def __repr__(self):
        return self.course_name

    # add student to Course instance
    def add_student_to_course(self, student):
        self.attending_students.append(student)
        return self.attending_students

    # add student to Course Register
    @staticmethod
    def add_student_to_register(student, register):
        register.add_student_to_course(student, student.courses[0])

    def give_grade(self, student, grade):
        if student in self.attending_students:
            student.get_grade(self, grade)
        else:
            print(f'{student} is not course attendee')

    def pass_course(self, student, grade):
        for student_ in self.attending_students:
            if student_ == student:
                self.attending_students.remove(student)
            else:
                pass
        self.graduates.append({student: grade})
        return self.attending_students, self.graduates


def main():
    class_reg = ClassroomRegister()
    student_reg = StudentRegister()
    course_reg = CourseRegister()

    parser = argparse.ArgumentParser()
    # print Classroom Register
    parser.add_argument('--print_class', '-pcl', action='store_true',
                        help='Print classroom register')
    # print Student Register
    parser.add_argument('--print_students', '-ps', action='store_true',
                        help='Print student register')
    # print Course Register
    parser.add_argument('--print_courses', '-pco', action='store_true',
                        help='Print courses register')
    # add new classroom to Classroom Register
    parser.add_argument('--new_classroom', '-newcl', nargs='*',
                        help='Add new classroom, give start year, end year')
    # add new student to Student Register
    parser.add_argument('--new_student', '-newst', nargs=5,
                        help='Add new student: give first name, last name, '
                             'date of birth yyyy-mm-dd, existing assigned '
                             'classroom, at least one existing course to '
                             'assign')
    # add new course to Course Register
    parser.add_argument('--new_course', '-newco', nargs='*',
                        help='Add new course, give course name, number of '
                             'grades to pass')
    # give grade to student
    parser.add_argument('--give_grade', '-grade', nargs=2,
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
        pass
    elif args.new_student:
        pass
    elif args.new_course:
        pass
    elif args.give_grade:
        pass


if __name__ == '__main__':
    main()
