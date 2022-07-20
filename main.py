
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

def ave_rate_all_students(course, *students):
    student_list = []
    for student in students:
        if student.grades.get(course):
            student_list.extend(student.grades[course])
    return round(sum(student_list) / len(student_list), 2)


def average_rate_all_lecturers(course, *lecturers):
    lector_list = []
    for lecturer in lecturers:
        if lecturer.rate_from_student.get(course):
            lector_list.extend(lecturer.rate_from_student[course])
    return round(sum(lector_list) / len(lector_list), 2)

# Студенты
student1 = Student('Patric', 'Boy', 'm')
student2 = Student('Venera', 'Sun', 'w')

# Студенты по курсам
student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Jira']
student2.courses_in_progress += ['Git']
student2.courses_in_progress += ['Python']


# Проверяющие экперты
reviewer_1 = Reviewer('Dima', 'Mendeleev')
reviewer_2 = Reviewer('Nic', 'Tesla')

# Эксперты по курсам
reviewer_1.courses_attached += ['Python']
reviewer_2.courses_attached += ['Jira']
reviewer_1.courses_attached += ['Git']

# Оценки за домашку
reviewer_1.rate_hw(student1, 'Python', 10)
reviewer_2.rate_hw(student1, 'Jira', 8)
reviewer_1.rate_hw(student2, 'Git', 10)
reviewer_1.rate_hw(student2, 'Python', 7)
reviewer_1.rate_hw(student2, 'Git', 9)

# Лекторы
lec_1 = Lecturer('Alexandr', 'Block')
lec_2 = Lecturer('Fedor', 'Dostoevskiy')

# Лекторы по курсам
lec_1.courses_attached += ['Python']
lec_1.courses_attached += ['Jira']
lec_2.courses_attached += ['Python']
lec_2.courses_attached += ['Jira']

# Оценки лекторам
student1.rate_lec(lec_1, 'Python', 10)
student2.rate_lec(lec_2, 'Python', 9)
student1.rate_lec(lec_2, 'Jira', 8)
student1.rate_lec(lec_2, 'Python', 6)
student2.rate_lec(lec_1, 'Python', 9)

print(f'\nСтудент: {student1}')
print(f'\nОценки: {student1.grades}')
print(f'\nЛектор: {lec_1}')
print(f'\nОценки студентов {lec_1.rate_from_student}')
print(f'\nПроверяющий: {reviewer_1}')
print()
print(student2 < lec_1)
print(student2 > lec_1)
print()
course = 'Python'
print(ave_rate_all_students(course, student1, student2))
print(average_rate_all_lecturers(course, lec_1, lec_2))