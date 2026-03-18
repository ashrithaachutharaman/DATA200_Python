import unittest
from AshrithaAchutharaman_Lab1 import Student, Course, Professor, LoginUser, CheckMyGradeSystem


class TestCheckMyGradeSystem(unittest.TestCase):

    def setUp(self):
        self.system = CheckMyGradeSystem()

        self.student1 = Student("S101", "Ashritha", "Achutharaman", "ash@example.com", ["C101"])
        self.student2 = Student("S102", "Meera", "Raman", "meera@example.com", ["C102"])

        self.course1 = Course("C101", "Python Programming", 3, "Spring", "MW", "10:00", "11:15", "In Person")
        self.course2 = Course("C102", "Data Structures", 4, "Fall", "TR", "1:00", "2:15", "Online")

        self.professor1 = Professor(
            "Dr. Rao",
            "rao@university.edu",
            "Associate Professor",
            ["C101"],
            {"2024": ["C100"]}
        )

        self.login1 = LoginUser("ash@example.com", "Password123", "student")

    def test_add_student(self):
        self.system.add_student(self.student1)
        self.assertIn("S101", self.system.students)
        self.assertEqual(self.system.students["S101"].first_name, "Ashritha")

    def test_add_course(self):
        self.system.add_course(self.course1)
        self.assertIn("C101", self.system.courses)
        self.assertEqual(self.system.courses["C101"].course_name, "Python Programming")

    def test_add_professor(self):
        self.system.add_professor(self.professor1)
        self.assertIn("rao@university.edu", self.system.professors)
        self.assertEqual(self.system.professors["rao@university.edu"].prof_name, "Dr. Rao")

    def test_delete_student(self):
        self.system.add_student(self.student1)
        self.system.delete_student("S101")
        self.assertNotIn("S101", self.system.students)

    def test_delete_course(self):
        self.system.add_course(self.course1)
        self.system.delete_course("C101")
        self.assertNotIn("C101", self.system.courses)

    def test_delete_professor(self):
        self.system.add_professor(self.professor1)
        self.system.delete_professor("rao@university.edu")
        self.assertNotIn("rao@university.edu", self.system.professors)

    def test_modify_student(self):
        self.system.add_student(self.student1)
        self.system.modify_student("S101", new_first_name="Asha", new_email="asha@example.com")
        self.assertEqual(self.system.students["S101"].first_name, "Asha")
        self.assertEqual(self.system.students["S101"].email, "asha@example.com")

    def test_modify_course(self):
        self.system.add_course(self.course1)
        self.system.modify_course("C101", new_course_name="Advanced Python", new_modality="Hybrid")
        self.assertEqual(self.system.courses["C101"].course_name, "Advanced Python")
        self.assertEqual(self.system.courses["C101"].modality, "Hybrid")

    def test_modify_professor(self):
        self.system.add_professor(self.professor1)
        self.system.modify_professor("rao@university.edu", new_prof_name="Dr. Raghav Rao")
        self.assertEqual(self.system.professors["rao@university.edu"].prof_name, "Dr. Raghav Rao")

    def test_search_student_by_id_found(self):
        self.system.add_student(self.student1)
        result = self.system.search_student_by_id("S101")
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "Ashritha")

    def test_search_student_by_id_not_found(self):
        result = self.system.search_student_by_id("S999")
        self.assertIsNone(result)

    def test_search_course_by_id_found(self):
        self.system.add_course(self.course1)
        result = self.system.search_course_by_id("C101")
        self.assertIsNotNone(result)
        self.assertEqual(result.course_name, "Python Programming")

    def test_search_professor_by_email_found(self):
        self.system.add_professor(self.professor1)
        result = self.system.search_professor_by_email("rao@university.edu")
        self.assertIsNotNone(result)
        self.assertEqual(result.prof_name, "Dr. Rao")

    def test_sort_students_by_name(self):
        self.system.add_student(self.student2)
        self.system.add_student(self.student1)
        sorted_students = self.system.sort_students_by_name()
        self.assertEqual(sorted_students[0].first_name, "Ashritha")
        self.assertEqual(sorted_students[1].first_name, "Meera")

    def test_sort_students_by_email(self):
        self.system.add_student(self.student2)
        self.system.add_student(self.student1)
        sorted_students = self.system.sort_students_by_email()
        self.assertEqual(sorted_students[0].email, "ash@example.com")
        self.assertEqual(sorted_students[1].email, "meera@example.com")

    def test_calculate_course_average(self):
        self.system.add_student(self.student1)
        self.system.add_student(self.student2)
        self.system.grades.add_course_grade("S101", "C101", "A", {"Quiz": 80, "Midterm": 90})
        self.system.grades.add_course_grade("S102", "C101", "B", {"Quiz": 70, "Midterm": 60})
        avg = self.system.calculate_course_average("C101")
        self.assertEqual(avg, 75)

    def test_calculate_course_median(self):
        self.system.add_student(self.student1)
        self.system.add_student(self.student2)
        self.system.grades.add_course_grade("S101", "C101", "A", {"Quiz": 80, "Midterm": 90})
        self.system.grades.add_course_grade("S102", "C101", "B", {"Quiz": 70, "Midterm": 60})
        median = self.system.calculate_course_median("C101")
        self.assertEqual(median, 75.0)

    def test_add_and_update_course_grade(self):
        self.system.grades.add_course_grade("S101", "C101", "B", {"Quiz": 75})
        self.system.grades.update_course_grade("S101", "C101", "A")
        self.system.grades.update_course_mark("S101", "C101", "Quiz", 95)
        self.assertEqual(self.system.grades.grade_records["S101"]["C101"]["grade"], "A")
        self.assertEqual(self.system.grades.grade_records["S101"]["C101"]["marks"]["Quiz"], 95)

    def test_encrypt_password(self):
        encrypted = self.login1.encrypt_password()
        self.assertNotEqual(encrypted, "Password123")

    def test_decrypt_password(self):
        encrypted = self.login1.encrypt_password()
        decrypted = self.login1.decrypt_password(encrypted)
        self.assertEqual(decrypted, "Password123")

    def test_login_user_success(self):
        self.system.add_login_user(self.login1)
        user = self.system.login_user("ash@example.com", "Password123")
        self.assertIsNotNone(user)
        self.assertTrue(user.is_logged_in)

    def test_login_user_failure(self):
        self.system.add_login_user(self.login1)
        user = self.system.login_user("ash@example.com", "WrongPassword")
        self.assertIsNotNone(user)
        self.assertFalse(user.is_logged_in)

    def test_large_student_dataset(self):
        for i in range(1000):
            student = Student(
                f"S{i}",
                f"First{i}",
                f"Last{i}",
                f"student{i}@example.com",
                []
            )
            self.system.add_student(student)

        self.assertEqual(len(self.system.students), 1000)
        self.assertIn("S500", self.system.students)
        self.assertEqual(self.system.students["S500"].email, "student500@example.com")


if __name__ == "__main__":
    unittest.main()