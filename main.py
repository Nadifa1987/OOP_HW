
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lec(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.rate_from_student:
                lecturer.rate_from_student[course] += [grade]
            else:
                lecturer.rate_from_student[course] = [grade]
        else:
            return 'Ошибка'

    def _ave_rate(self, grade):
        ave_rate = []
        courses = []
        for key, value in self.grades.items():
            ave_rate += value
            if key not in courses:
                courses.append(key)
            else:
                courses += key
        mean = round((sum(ave_rate) / len(ave_rate)), 2)
        if grade == 'grade':
            return mean
        elif grade == 'graded_courses':
            return courses

    def __str__(self):
        grade = 'grade'
        graded_courses = 'graded_courses'
        res = (f"\nИмя: {self.name}"
               f"\nФамилия: {self.surname}"
               f"\nСредняя оценка за домашние задания: {self._ave_rate(grade)}"
               f"\nКурсы в процессе изучения: {', '.join(self._ave_rate(graded_courses))}"
               f"\nЗавершенные курсы: {', '.join(self.finished_courses)}")
        return res

    def __lt__(self, other):
        grade = 'grade'
        if not isinstance(other, Lecturer):
            return f'не тот человек для сравнения'
        return self._ave_rate(grade) < other.ave_rate_from_student()

    def __gt__(self, other):
        grade = 'grade'
        if not isinstance(other, Lecturer):
            return f'не тот человек для сравнения'
        return self._ave_rate(grade) > other.ave_rate_from_student()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.rate_from_student = {}

    def ave_rate_from_student(self):
        ave_rate_from_student = []
        for key, value in self.rate_from_student.items():
            ave_rate_from_student += value
        mean = round((sum(ave_rate_from_student) / len(ave_rate_from_student)), 2)
        return mean

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.ave_rate_from_student()}'
        return res

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res