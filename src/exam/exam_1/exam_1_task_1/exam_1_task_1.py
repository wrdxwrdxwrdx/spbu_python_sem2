from datetime import date
from typing import Optional


class Person:
    def __init__(self, full_name: str, birthday: date, info: str = "") -> None:
        self.full_name = full_name
        self.birthday = birthday
        self.info = info


class Subject:
    def __init__(self, name: str, number_of_hours: float):
        self.name = name
        self.number_of_hours = number_of_hours

    def __str__(self) -> str:
        return f"Subject {self.name}"

    def __repr__(self) -> str:
        return f"Subject {self.name}({self.number_of_hours}h)"


class Student(Person):
    def __init__(
        self, full_name: str, birthday: date, grades: Optional[dict[Subject, float]] = None, info: str = ""
    ) -> None:
        super().__init__(full_name, birthday, info)
        self.grades = grades if grades else {}

    def modify_subject_grade(self, subject: Subject, grade: float) -> None:
        self.grades[subject] = grade

    def __str__(self) -> str:
        return f"Student {self.full_name}, DOB: {self.birthday}"

    def __repr__(self) -> str:
        return f"Student {self.full_name}, DOB: {self.birthday}, grades: {self.grades}, info: {self.info} "


class Teacher(Person):
    def __init__(self, full_name: str, birthday: date, subjects: Optional[set[Subject]] = None, info: str = "") -> None:
        super().__init__(full_name, birthday, info)
        self.subjects = subjects if subjects else set()

    def add_subject(self, subject: Subject) -> None:
        self.subjects.add(subject)

    def remove_subject(self, subject: Subject) -> None:
        if subject not in self.subjects:
            raise KeyError(f"{self} does not teach {subject})")
        self.subjects.remove(subject)

    def __str__(self) -> str:
        return f"Teacher {self.full_name}, DOB: {self.birthday})"

    def __repr__(self) -> str:
        return f"Teacher {self.full_name}, DOB: {self.birthday}, subjects: {self.subjects}"


class University:
    def __init__(self) -> None:
        self.students: dict[str, list[Student]] = {}
        self.teachers: dict[str, list[Teacher]] = {}
        self.subjects: dict[str, Subject] = {}

    def add_new_subject(self, name: str, number_of_hours: float) -> None:
        self.subjects[name] = Subject(name, number_of_hours)

    def add_new_student(
        self, full_name: str, birthday: date, grades: Optional[dict[str, float]] = None, info: str = ""
    ) -> None:
        grades = grades if grades else dict()
        grades_obj = dict()
        for subject in grades:
            if subject in self.subjects:
                grades_obj[self.subjects[subject]] = grades[subject]
            else:
                raise KeyError(f"There is no {subject} in university program")
        student = Student(full_name, birthday, grades_obj, info)
        if full_name in self.students:
            self.students[full_name].append(student)
        else:
            self.students[full_name] = [student]

    def add_new_teacher(
        self, full_name: str, birthday: date, subjects: Optional[set[str]] = None, info: str = ""
    ) -> None:
        subjects = subjects if subjects else set()
        subjects_obj = set(self.subjects[subject] for subject in subjects)
        teacher = Teacher(full_name, birthday, subjects_obj, info)
        if full_name in self.teachers:
            self.teachers[full_name].append(teacher)
        else:
            self.teachers[full_name] = [teacher]

    def get_teacher_subjects(self, full_name: str) -> dict[Teacher, list[Subject]]:
        if full_name not in self.teachers:
            raise KeyError(f"There is no Teacher {full_name} in university")
        output = {}
        for teacher in self.teachers[full_name]:
            output[teacher] = list(teacher.subjects)
        return output

    def get_student_subjects(self, full_name: str) -> dict[Student, list[Subject]]:
        if full_name not in self.students:
            raise KeyError(f"There is no Student {full_name} in university")
        output = {}
        for student in self.students[full_name]:
            output[student] = list(student.grades.keys())
        return output

    def get_average_grade(self, full_name: str) -> dict[Student, float]:
        if full_name not in self.students:
            raise KeyError(f"There is no Student {full_name} in university")
        output = {}
        for student in self.students[full_name]:
            output[student] = sum(student.grades.values()) / len(student.grades)
        return output

    def modify_subject_grade(self, subject: str, full_name: str, birthday: date, grade: float) -> None:
        if subject not in self.subjects:
            raise KeyError(f"There is no {subject} in university program")
        if full_name not in self.students:
            raise KeyError(f"There is no Student {full_name} in university")
        for student in self.students[full_name]:
            if student.birthday == birthday:
                student.modify_subject_grade(self.subjects[subject], grade)
                break
        else:
            raise KeyError(f"No Student {full_name} with DOB {birthday}")

    def add_teacher_subject(self, subject: str, full_name: str, birthday: date) -> None:
        if subject not in self.subjects:
            raise KeyError(f"There is no {subject} in university program")
        if full_name not in self.teachers:
            raise KeyError(f"There is no Teacher {full_name} in university")
        for teacher in self.teachers[full_name]:
            if teacher.birthday == birthday:
                teacher.add_subject(self.subjects[subject])
                break
        else:
            raise KeyError(f"No Teacher {full_name} with DOB {birthday}")

    def remove_teacher_subject(self, subject: str, full_name: str, birthday: date) -> None:
        if subject not in self.subjects:
            raise KeyError(f"There is no {subject} in university program")
        if full_name not in self.teachers:
            raise KeyError(f"There is no Teacher {full_name} in university")
        for teacher in self.teachers[full_name]:
            if teacher.birthday == birthday:
                teacher.remove_subject(self.subjects[subject])
                break
        else:
            raise KeyError(f"No Teacher {full_name} with DOB {birthday}")


if __name__ == "__main__":
    university = University()
    university.add_new_subject("math", 30)
    university.add_new_subject("physics", 25)
    university.add_new_student("Romanyuk Artem Dmitrievich", date(2006, 5, 16))
    university.add_new_teacher("Kozlov Maxim Klimovich", date(2006, 5, 16))
    university.add_teacher_subject("math", "Kozlov Maxim Klimovich", date(2006, 5, 16))
    university.add_teacher_subject("physics", "Kozlov Maxim Klimovich", date(2006, 5, 16))
    university.modify_subject_grade("math", "Romanyuk Artem Dmitrievich", date(2006, 5, 16), 98)
    university.modify_subject_grade("physics", "Romanyuk Artem Dmitrievich", date(2006, 5, 16), 35)

    print(university.get_average_grade("Romanyuk Artem Dmitrievich"))
    print(university.get_teacher_subjects("Kozlov Maxim Klimovich"))
    print(university.get_student_subjects("Romanyuk Artem Dmitrievich"))
