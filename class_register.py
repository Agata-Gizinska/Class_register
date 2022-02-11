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

    def __repr__(self):
        return f'Class {self.name}'

    def add_student(self, student):
        self.student_list.append(student)
        return self.student_list

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

    def __init__(self, first_name, last_name, birth_day, birth_month,
                 birth_year, classroom):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.fullname = f'{first_name} {last_name}'
        self.birth_day = int(birth_day)
        self.birth_month = int(birth_month)
        self.birth_year = int(birth_year)
        self.birth_date = datetime.date(self.birth_year, self.birth_month,
                                        self.birth_day)
        self.classroom = classroom
        self.status = 'Active'
        self.courses = []
        classroom.add_student(self)  # student is automatically added to
        # prompted classroom

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
        else:
            pass

    def drop_out(self):
        self.status = 'Inactive'
        self.classroom.drop_out_student(self)


class Course:

    def __init__(self, course_name, partial_grades_num):
        self.course_name = course_name
        self.attending_students = []
        self.graduates = []
        self.drop_outs = []
        self.len_partial = int(partial_grades_num)

    def __repr__(self):
        return self.course_name

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
    pass


if __name__ == '__main__':
    main()
