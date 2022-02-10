#!/usr/bin/python3
import datetime


class Classroom:

    def __init__(self, start_year, end_year):
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        self.name = f'{start_year}-{end_year}'
        self.years_num = end_year - start_year
        self.student_list = []
        self.drop_out_list = []
        self.graduates = []

    def add_student(self, student):
        self.student_list.append(student)
        return self.student_list

    def drop_out_student(self, student):
        self.student_list.remove(student)
        self.drop_out_list.append(student)
        return self.student_list, self.drop_out_list


class Student:

    def __init__(self, first_name, last_name, birth_day, birth_month, birth_year, classroom):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.fullname = f'{first_name} {last_name}'
        self.birth_day = int(birth_day)
        self.birth_month = int(birth_month)
        self.birth_year = int(birth_year)
        self.birth_date = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        self.classroom = classroom
        self.status = 'Active'
        self.courses = []
        classroom.add_student(self)

    def __repr__(self):
        return self.fullname

    def add_course(self, course):
        self.courses.append({course: []})
        course.attending_students.append(self)
        return self.courses

    def get_grade(self, course, grade):
        pass

    def pass_course(self, course, grades):
        pass

    def graduate(self):
        pass

    def drop_out(self):
        self.status = 'Inactive'
        self.classroom.drop_out_list.append(self)


class Course:

    def __init__(self, course_name):
        self.course_name = course_name
        self.attending_students = []
        self.graduates = []

    def __repr__(self):
        return self.course_name

    def give_grade(self, student, grade):
        student.get_grade(self, grade)

    def pass_course(self, student, grade):
        self.attending_students.remove(student)
        self.graduates.append({student: grade})
        return self.attending_students, self.graduates


def main():
    pass


if __name__ == '__main__':
    main()
