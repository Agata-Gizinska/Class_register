# Class_register

Manage your students, their courses and grades!

## General info

This program allows to manage data in three csv files, each handling different databases: Classroom Register (classrooms.csv), Students Register (students.csv) and Course Register (courses.csv).

The Classroom Register contains information about available classrooms (in the meaning of class of students, not to mistake with class in programming languages!), such as their names, start year, planned graduation year, the lists of active students, graduates and dropout students.

The Student Register contains information about each student, such as their first name, last name, date of birth, assigned classroom, assigned courses and their status.

The Course Register contains information about all available courses that students may attend to. The register includes course's name, number of grades required to pass the course, the lists of attending students, graduates for the course and dropout students.

The program is based on argument parser which allows you to:
- view the current state of each register,
- update registers by adding new elements: new classrooms, new courses and new students,
- append students to new courses,
- give grades to students.

The default settings of program mechanics are based on certain assumptions:
- Each student has to pass 3 courses in total to graduate from the classroom.
- Students are not allowed to fail any of the courses. If they do, they are dropped out from the classroom.
- Students can get grades: 2, 3, 4, 5 (from the worst to the best score).
- To pass a course the student has to get a final grade equal to or higher than 3.
- Final grade is calculated as a mean of all grades that the student got for the course rounded to the nearest integer.

## Technology

- Python 3.8

## Usage

Using the terminal change the current directory to the directory with the class_register.py file. Run an appropriate command.

Available commands:

```python class_register.py print_register {register: [classrooms, students, courses]}```

```python class_register.py new_classroom {start year} {end year}```

```python class_register.py new_student {first name} {last name} {date of birth} {assigned classroom} {first course}```

```python class_register.py new_course {course name} {required number of grades}```

```python class_register.py append_to_course {first name} {last name} {course name}```

```python class_register.py give_grade {first name} {last name} {course name} {grade: [2, 3, 4, 5]}```

Use command ```python class_register.py --help``` to get help messages. You may also get help messages for each option, for example:

```python class_register.py give_grade --help```
