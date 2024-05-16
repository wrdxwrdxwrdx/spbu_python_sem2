import pytest

from src.exam.exam_1.exam_1_task_1.exam_1_task_1 import *


class TestSubject:
    @pytest.mark.parametrize("name,number_of_hours", (("Math", 30), ("Physics", 20), ("English", 27.5)))
    def test_str_repr(self, name, number_of_hours):
        subject = Subject(name, number_of_hours)
        assert str(subject) == f"Subject {name}"
        assert repr(subject) == f"Subject {name}({number_of_hours}h)"


class TestStudent:
    s1 = Subject("1", 1)
    s2 = Subject("2", 2)
    s3 = Subject("3", 3)
    s4 = Subject("4", 4)
    s5 = Subject("5", 5)

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {s1: 12.2}, "Hello"),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {s2: 123}, "S"),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {s3: 123}, "O"),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {s1: 1, s2: 2}, "S"),
        ),
    )
    def test_str_repr(self, full_name, birthday, grades, info):
        student = Student(full_name, birthday, grades, info)
        assert str(student) == f"Student {full_name}, DOB: {birthday}"
        assert repr(student) == f"Student {full_name}, DOB: {birthday}, grades: {grades}, info: {info} "

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info,subject,grade",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {s1: 12.2}, "Hello", s1, 100),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {s2: 123}, "S", s2, 12),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), None, "O", s3, 11.2),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), None, "S", s5, 1233),
        ),
    )
    def test_modify_subject_grade(self, full_name, birthday, grades, info, subject, grade):
        student = Student(full_name, birthday, grades, info)
        student.modify_subject_grade(subject, grade)
        assert student.grades[subject] == grade


class TestTeacher:
    s1 = Subject("1", 1)
    s2 = Subject("2", 2)
    s3 = Subject("3", 3)
    s4 = Subject("4", 4)
    s5 = Subject("5", 5)

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {s1, s4}, "Hello"),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {s2}, "S"),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {s3}, "O"),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {s1, s2, s5}, "S"),
        ),
    )
    def test_str_repr(self, full_name, birthday, subjects, info):
        teacher = Teacher(full_name, birthday, subjects, info)
        assert str(teacher) == f"Teacher {full_name}, DOB: {birthday})"
        assert repr(teacher) == f"Teacher {full_name}, DOB: {birthday}, subjects: {subjects}"

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info,new_subject",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {s1, s4}, "Hello", s2),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {s2}, "S", s2),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {s3}, "O", s1),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {s1, s2, s5}, "S", s3),
        ),
    )
    def test_add_subject(self, full_name, birthday, subjects, info, new_subject):
        teacher = Teacher(full_name, birthday, subjects, info)
        teacher.add_subject(new_subject)
        assert new_subject in teacher.subjects

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info,remove_subject",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {s1, s4}, "Hello", s1),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {s2}, "S", s2),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {s3}, "O", s3),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {s1, s2, s5}, "S", s5),
        ),
    )
    def test_remove_subject(self, full_name, birthday, subjects, info, remove_subject):
        teacher = Teacher(full_name, birthday, subjects, info)
        teacher.remove_subject(remove_subject)
        assert remove_subject not in teacher.subjects

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {s1, s4}, "Hello"),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {s2}, "S"),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {s3}, "O"),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {s1, s2, s5}, "S"),
        ),
    )
    def test_exception_remove_subject(self, full_name, birthday, subjects, info):
        with pytest.raises(KeyError):
            teacher = Teacher(full_name, birthday, subjects, info)
            teacher.remove_subject(Subject("smth", 123))


class TestUniversity:
    s1 = Subject("1", 1)
    s2 = Subject("2", 2)
    s3 = Subject("3", 3)
    s4 = Subject("4", 4)
    s5 = Subject("5", 5)

    @pytest.mark.parametrize("name,number_of_hours", (("Math", 30), ("Physics", 20), ("English", 27.5)))
    def test_add_new_subject(self, name, number_of_hours):
        university = University()
        university.add_new_subject(name, number_of_hours)
        assert university.subjects[name].name == name
        assert university.subjects[name].number_of_hours == number_of_hours

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2}, "Hello"),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123}, "S"),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123}, "O"),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S"),
        ),
    )
    def test_add_new_student(self, full_name, birthday, grades, info):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        grades_obj = {}
        for subject in grades:
            grades_obj[university.subjects[subject]] = grades[subject]
        assert university.students[full_name][0].full_name == full_name
        assert university.students[full_name][0].birthday == birthday
        assert university.students[full_name][0].grades == grades_obj
        assert university.students[full_name][0].info == info

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s11": 12.2}, "Hello"),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s21": 123}, "S"),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s31": 123}, "O"),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s11": 1, "s2": 2}, "S"),
        ),
    )
    def test_exception_add_new_student(self, full_name, birthday, grades, info):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        with pytest.raises(KeyError):
            university.add_new_student(full_name, birthday, grades, info)

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1", "s4"}, "Hello"),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2"}, "S"),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3"}, "O"),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1", "s2", "s5"}, "S"),
        ),
    )
    def test_add_new_teacher(self, full_name, birthday, subjects, info):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_teacher(full_name, birthday, subjects, info)
        assert university.teachers[full_name][0].full_name == full_name
        assert university.teachers[full_name][0].birthday == birthday
        assert university.teachers[full_name][0].info == info

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info,expected",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1", "s4"}, "Hello", [s1, s4]),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2"}, "S", [s2]),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3"}, "O", [s3]),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1", "s2", "s5"}, "S", [s1, s2, s5]),
        ),
    )
    def test_get_teacher_subjects(self, full_name, birthday, subjects, info, expected):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_teacher(full_name, birthday, subjects, info)
        subjects = list(university.get_teacher_subjects(full_name).values())[0]
        for subject in subjects:
            assert subject in expected

    @pytest.mark.parametrize(
        "full_name,birthday,subjects,info,expected",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1", "s4"}, "Hello", [s1, s4]),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2"}, "S", [s2]),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3"}, "O", [s3]),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1", "s2", "s5"}, "S", [s1, s2, s5]),
        ),
    )
    def test_exception_get_teacher_subjects(self, full_name, birthday, subjects, info, expected):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_teacher(full_name, birthday, subjects, info)
        with pytest.raises(KeyError):
            subjects = list(university.get_teacher_subjects(full_name + "HEHE").values())[0]

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info, expected",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2}, "Hello", [s1]),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123}, "S", [s2]),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123}, "O", [s3]),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", [s1, s2]),
        ),
    )
    def test_get_student_subjects(self, full_name, birthday, grades, info, expected):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        subjects = list(university.get_student_subjects(full_name).values())[0]
        for subject in subjects:
            assert subject in expected

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info, expected",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2}, "Hello", [s1]),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123}, "S", [s2]),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123}, "O", [s3]),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", [s1, s2]),
        ),
    )
    def test_exception_get_student_subjects(self, full_name, birthday, grades, info, expected):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        with pytest.raises(KeyError):
            subjects = list(university.get_student_subjects(full_name + "HEHE").values())[0]

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info, expected",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2, "s5": 12}, "Hello", [s1]),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123, "s5": 15}, "S", [s2]),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123, "s5": 1.32}, "O", [s3]),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", [s1, s2]),
        ),
    )
    def test_get_average_grade(self, full_name, birthday, grades, info, expected):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        avg = university.get_average_grade(full_name)
        assert list(avg.values())[0] == sum(grades.values()) / len(grades)

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info, expected",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2, "s5": 12}, "Hello", [s1]),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123, "s5": 15}, "S", [s2]),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123, "s5": 1.32}, "O", [s3]),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", [s1, s2]),
        ),
    )
    def test_exception_get_average_grade(self, full_name, birthday, grades, info, expected):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        with pytest.raises(KeyError):
            avg = university.get_average_grade(full_name + "HEHE")

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info,subject,new_grade",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2, "s5": 12}, "Hello", "s3", 123),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123, "s5": 15}, "S", "s3", 123),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123, "s5": 1.32}, "O", "s3", 123),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", "s1", 123),
        ),
    )
    def test_modify_subject_grade(self, full_name, birthday, grades, info, subject, new_grade):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        university.modify_subject_grade(subject, full_name, birthday, new_grade)
        assert new_grade in university.students[full_name][0].grades.values()

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info,subject,new_grade",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2, "s5": 12}, "Hello", "s33", 123),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123, "s5": 15}, "S", "s23", 123),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123, "s5": 1.32}, "O", "s43", 123),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", "s15", 123),
        ),
    )
    def test_exception_subject_modify_subject_grade(self, full_name, birthday, grades, info, subject, new_grade):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        with pytest.raises(KeyError):
            university.modify_subject_grade(subject, full_name, birthday, new_grade)

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info,subject,new_grade",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2, "s5": 12}, "Hello", "s3", 123),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123, "s5": 15}, "S", "s3", 123),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123, "s5": 1.32}, "O", "s4", 123),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", "s1", 123),
        ),
    )
    def test_exception_name_modify_subject_grade(self, full_name, birthday, grades, info, subject, new_grade):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        with pytest.raises(KeyError):
            university.modify_subject_grade(subject, full_name + "HEHE", birthday, new_grade)

    @pytest.mark.parametrize(
        "full_name,birthday,grades,info,subject,new_grade",
        (
            ("Romanyuk Artem Dmitrievich", date(2006, 5, 16), {"s1": 12.2, "s5": 12}, "Hello", "s3", 123),
            ("Yakovleva Milana Maksimovna", date(2002, 11, 1), {"s2": 123, "s5": 15}, "S", "s3", 123),
            ("Soloviev Maxim Markovich", date(2000, 10, 10), {"s3": 123, "s5": 1.32}, "O", "s4", 123),
            ("Kozlov Maxim Klimovich", date(2001, 1, 22), {"s1": 1, "s2": 2}, "S", "s1", 123),
        ),
    )
    def test_exception_date_modify_subject_grade(self, full_name, birthday, grades, info, subject, new_grade):
        university = University()
        university.subjects = {"s1": self.s1, "s2": self.s2, "s3": self.s3, "s4": self.s4, "s5": self.s5}
        university.add_new_student(full_name, birthday, grades, info)
        with pytest.raises(KeyError):
            university.modify_subject_grade(subject, full_name, date(1001, 1, 22), new_grade)
