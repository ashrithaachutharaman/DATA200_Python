import csv
import time
import statistics


class Student:
    def __init__(self, student_id, first_name, last_name, email, courses=None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.courses = courses if courses is not None else []

    def add_course(self, course_id):
        if course_id in self.courses:
            print("Course already added to schedule.")
        else:
            self.courses.append(course_id)
            print("Course added successfully.")

    def delete_course(self, course_id):
        if course_id in self.courses:
            self.courses.remove(course_id)
            print("Course removed successfully.")
        else:
            print("Course not found.")

    def display_records(self):
        print(f"Student ID: {self.student_id}")
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Email: {self.email}")

        if not self.courses:
            print("No courses enrolled.")
        else:
            print("Enrolled Courses:")
            for course_id in self.courses:
                print(f"  {course_id}")


class Course:
    def __init__(self, course_id, course_name, course_creds, term, days, start_time, end_time, modality):
        self.course_id = course_id
        self.course_name = course_name
        self.course_creds = course_creds
        self.term = term
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.modality = modality

    def display_course_details(self):
        print("COURSE DETAILS:")
        print(f"Course ID: {self.course_id}")
        print(f"Course Name: {self.course_name}")
        print(f"Number of Credits: {self.course_creds}")
        print(f"Term Offered: {self.term}")
        print(f"Days of Class: {self.days}")
        print(f"Start Time: {self.start_time}")
        print(f"End Time: {self.end_time}")
        print(f"Mode of Class: {self.modality}")


class Professor:
    def __init__(self, prof_name, prof_email, prof_rank, current_courses=None, past_courses=None):
        self.prof_name = prof_name
        self.prof_email = prof_email
        self.prof_rank = prof_rank
        self.current_courses = current_courses if current_courses is not None else []
        self.past_courses = past_courses if past_courses is not None else {}

    def prof_details(self):
        print(f"Professor Name: {self.prof_name}")
        print(f"Professor Email: {self.prof_email}")
        print(f"Professor Rank: {self.prof_rank}")

    def prof_course_details(self):
        print(f"Courses for Professor: {self.prof_name}")

        if not self.current_courses:
            print("Current Courses: None")
        else:
            print("Current Courses:")
            for course_id in self.current_courses:
                print(f"  {course_id}")

        if not self.past_courses:
            print("Previously Taught Courses: None")
        else:
            print("Past Courses:")
            for year in self.past_courses:
                print(f"  {year}:")
                for course_id in self.past_courses[year]:
                    print(f"    {course_id}")


class Grades:
    def __init__(self):
        self.grade_records = {}

    def add_student_record(self, student_id):
        if student_id not in self.grade_records:
            self.grade_records[student_id] = {}

    def add_course_grade(self, student_id, course_id, course_grade="Not Available Yet", marks=None):
        if student_id not in self.grade_records:
            self.grade_records[student_id] = {}

        self.grade_records[student_id][course_id] = {
            "grade": course_grade,
            "marks": marks if marks is not None else {}
        }

    def delete_course_grade(self, student_id, course_id):
        if student_id in self.grade_records and course_id in self.grade_records[student_id]:
            del self.grade_records[student_id][course_id]
            print("Grade record deleted successfully.")
        else:
            print("Course or student not found in records.")

    def update_course_grade(self, student_id, course_id, new_grade):
        if student_id in self.grade_records and course_id in self.grade_records[student_id]:
            self.grade_records[student_id][course_id]["grade"] = new_grade
            print("Grade updated successfully.")
        else:
            print("Course or student not found in records.")

    def update_course_mark(self, student_id, course_id, item, new_score):
        if student_id in self.grade_records and course_id in self.grade_records[student_id]:
            self.grade_records[student_id][course_id]["marks"][item] = new_score
            print("Marks have been updated successfully.")
        else:
            print("Course or student not found in records.")

    def show_student_grades(self, student_id):
        if student_id not in self.grade_records or not self.grade_records[student_id]:
            print("No grade records available for this student.")
        else:
            print(f"Grade records for Student ID: {student_id}")
            for course_id in self.grade_records[student_id]:
                grade = self.grade_records[student_id][course_id]["grade"]
                print(f"{course_id}: {grade}")

    def show_student_marks(self, student_id):
        if student_id not in self.grade_records or not self.grade_records[student_id]:
            print("No marks available for this student.")
        else:
            print(f"Marks for Student ID: {student_id}")
            for course_id in self.grade_records[student_id]:
                print(f"Course ID: {course_id}")
                marks = self.grade_records[student_id][course_id]["marks"]

                if not marks:
                    print("No marks available.")
                else:
                    for item in marks:
                        print(f"  {item}: {marks[item]}")

    def show_student_report(self, student_id):
        if student_id not in self.grade_records or not self.grade_records[student_id]:
            print("No report available for this student.")
        else:
            print(f"FINAL REPORT FOR STUDENT ID: {student_id}")
            for course_id in self.grade_records[student_id]:
                print(f"\nCourse ID: {course_id}")
                print(f"Grade: {self.grade_records[student_id][course_id]['grade']}")
                print("Marks:")

                marks = self.grade_records[student_id][course_id]["marks"]
                if not marks:
                    print("No marks available yet.")
                else:
                    for item in marks:
                        print(f"  {item}: {marks[item]}")


class LoginUser:
    def __init__(self, email_id, password, role):
        self.email_id = email_id
        self.password = password
        self.role = role
        self.is_logged_in = False

    def encrypt_password(self):
        encrypted_chars = []
        for ch in self.password:
            encrypted_chars.append(chr(ord(ch) + 3))
        return "".join(encrypted_chars)

    def decrypt_password(self, encrypted_password):
        decrypted_chars = []
        for ch in encrypted_password:
            decrypted_chars.append(chr(ord(ch) - 3))
        return "".join(decrypted_chars)

    def login(self, entered_password, encrypted_password):
        original_password = self.decrypt_password(encrypted_password)

        if entered_password == original_password:
            self.is_logged_in = True
            print("Login successful!")
        else:
            print("Invalid password.")

    def logout(self):
        if self.is_logged_in:
            self.is_logged_in = False
            print("Logout successful.")
        else:
            print("User is not logged in.")

    def change_password(self, old_password, new_password):
        if old_password == self.password:
            self.password = new_password
            print("Password changed successfully!")
        else:
            print("Password is incorrect.")


class CheckMyGradeSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.professors = {}
        self.logins = {}
        self.grades = Grades()

    # -------------------------
    # ADD METHODS
    # -------------------------
    def add_student(self, student):
        if not student.student_id:
            print("Student ID cannot be null.")
            return
        if student.student_id in self.students:
            print("Student ID must be unique.")
            return
        self.students[student.student_id] = student
        print("Student added successfully.")

    def add_course(self, course):
        if not course.course_id:
            print("Course ID cannot be null.")
            return
        if course.course_id in self.courses:
            print("Course ID must be unique.")
            return
        self.courses[course.course_id] = course
        print("Course added successfully.")

    def add_professor(self, professor):
        if not professor.prof_email:
            print("Professor email/ID cannot be null.")
            return
        if professor.prof_email in self.professors:
            print("Professor ID must be unique.")
            return
        self.professors[professor.prof_email] = professor
        print("Professor added successfully.")

    def add_login_user(self, login_user):
        if login_user.email_id in self.logins:
            print("Login user already exists.")
            return

        self.logins[login_user.email_id] = {
            "password": login_user.encrypt_password(),
            "role": login_user.role
        }
        print("Login user added successfully.")

    # -------------------------
    # LOGIN
    # -------------------------
    def login_user(self, email_id, entered_password):
        if email_id in self.logins:
            encrypted_password = self.logins[email_id]["password"]
            role = self.logins[email_id]["role"]

            user = LoginUser(email_id, "", role)
            user.login(entered_password, encrypted_password)
            return user
        else:
            print("User not found.")
            return None

    # -------------------------
    # STUDENT CSV
    # -------------------------
    def save_students_to_csv(self, filename="students.csv"):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student_id", "first_name", "last_name", "email", "courses"])

            for student_id in self.students:
                student = self.students[student_id]
                courses_text = "|".join(student.courses)

                writer.writerow([
                    student.student_id,
                    student.first_name,
                    student.last_name,
                    student.email,
                    courses_text
                ])

    def load_students_from_csv(self, filename="students.csv"):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                student_id = row[0]
                first_name = row[1]
                last_name = row[2]
                email = row[3]
                courses_text = row[4]

                courses = courses_text.split("|") if courses_text else []
                student = Student(student_id, first_name, last_name, email, courses)
                self.students[student_id] = student

    # -------------------------
    # COURSE CSV
    # -------------------------
    def save_courses_to_csv(self, filename="courses.csv"):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "course_id",
                "course_name",
                "course_creds",
                "term",
                "days",
                "start_time",
                "end_time",
                "modality"
            ])

            for course_id in self.courses:
                course = self.courses[course_id]

                writer.writerow([
                    course.course_id,
                    course.course_name,
                    course.course_creds,
                    course.term,
                    course.days,
                    course.start_time,
                    course.end_time,
                    course.modality
                ])

    def load_courses_from_csv(self, filename="courses.csv"):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                course_id = row[0]
                course_name = row[1]
                course_creds = row[2]
                term = row[3]
                days = row[4]
                start_time = row[5]
                end_time = row[6]
                modality = row[7]

                course = Course(
                    course_id,
                    course_name,
                    course_creds,
                    term,
                    days,
                    start_time,
                    end_time,
                    modality
                )
                self.courses[course_id] = course

    # -------------------------
    # PROFESSOR CSV
    # -------------------------
    def save_professors_to_csv(self, filename="professor.csv"):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "prof_name",
                "prof_email",
                "prof_rank",
                "current_courses",
                "past_courses"
            ])

            for prof_email in self.professors:
                professor = self.professors[prof_email]
                current_courses_text = "|".join(professor.current_courses)

                past_courses_list = []
                for year in professor.past_courses:
                    courses_text = ",".join(professor.past_courses[year])
                    past_courses_list.append(f"{year}:{courses_text}")

                past_courses_text = "|".join(past_courses_list)

                writer.writerow([
                    professor.prof_name,
                    professor.prof_email,
                    professor.prof_rank,
                    current_courses_text,
                    past_courses_text
                ])

    def load_professors_from_csv(self, filename="professor.csv"):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                prof_name = row[0]
                prof_email = row[1]
                prof_rank = row[2]
                current_courses_text = row[3]
                past_courses_text = row[4]

                current_courses = current_courses_text.split("|") if current_courses_text else []

                past_courses = {}
                if past_courses_text:
                    past_entries = past_courses_text.split("|")
                    for entry in past_entries:
                        year, courses_text = entry.split(":")
                        past_courses[year] = courses_text.split(",") if courses_text else []

                professor = Professor(
                    prof_name,
                    prof_email,
                    prof_rank,
                    current_courses,
                    past_courses
                )
                self.professors[prof_email] = professor

    # -------------------------
    # LOGIN CSV
    # -------------------------
    def save_logins_to_csv(self, filename="login.csv"):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["email_id", "password", "role"])
            for email_id in self.logins:
                login_record = self.logins[email_id]

                writer.writerow([
                    email_id,
                    login_record["password"],
                    login_record["role"]
                ])

    def load_logins_from_csv(self, filename="login.csv"):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                email_id = row[0]
                password = row[1]
                role = row[2]

                self.logins[email_id] = {
                    "password": password,
                    "role": role
                }

    # -------------------------
    # DELETE METHODS
    # -------------------------
    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def delete_course(self, course_id):
        if course_id in self.courses:
            del self.courses[course_id]
            print("Course deleted successfully.")
        else:
            print("Course not found.")

    def delete_professor(self, prof_email):
        if prof_email in self.professors:
            del self.professors[prof_email]
            print("Professor deleted successfully.")
        else:
            print("Professor not found.")

    def delete_login_user(self, email_id):
        if email_id in self.logins:
            del self.logins[email_id]
            print("Login user deleted successfully.")
        else:
            print("Login user not found.")

    # -------------------------
    # MODIFY METHODS
    # -------------------------
    def modify_student(self, student_id, new_first_name=None, new_last_name=None, new_email=None, new_courses=None):
        if student_id in self.students:
            student = self.students[student_id]

            if new_first_name is not None:
                student.first_name = new_first_name
            if new_last_name is not None:
                student.last_name = new_last_name
            if new_email is not None:
                student.email = new_email
            if new_courses is not None:
                student.courses = new_courses

            print("Student record updated successfully.")
        else:
            print("Student not found.")

    def modify_course(self, course_id, new_course_name=None, new_course_creds=None, new_term=None,
                      new_days=None, new_start_time=None, new_end_time=None, new_modality=None):
        if course_id in self.courses:
            course = self.courses[course_id]

            if new_course_name is not None:
                course.course_name = new_course_name
            if new_course_creds is not None:
                course.course_creds = new_course_creds
            if new_term is not None:
                course.term = new_term
            if new_days is not None:
                course.days = new_days
            if new_start_time is not None:
                course.start_time = new_start_time
            if new_end_time is not None:
                course.end_time = new_end_time
            if new_modality is not None:
                course.modality = new_modality

            print("Course record updated successfully.")
        else:
            print("Course not found.")

    def modify_professor(self, prof_email, new_prof_name=None, new_prof_rank=None,
                         new_current_courses=None, new_past_courses=None):
        if prof_email in self.professors:
            professor = self.professors[prof_email]

            if new_prof_name is not None:
                professor.prof_name = new_prof_name
            if new_prof_rank is not None:
                professor.prof_rank = new_prof_rank
            if new_current_courses is not None:
                professor.current_courses = new_current_courses
            if new_past_courses is not None:
                professor.past_courses = new_past_courses

            print("Professor record updated successfully.")
        else:
            print("Professor not found.")

    def modify_login_user(self, email_id, new_password=None, new_role=None):
        if email_id in self.logins:
            if new_password is not None:
                temp_user = LoginUser(email_id, new_password, self.logins[email_id]["role"])
                self.logins[email_id]["password"] = temp_user.encrypt_password()

            if new_role is not None:
                self.logins[email_id]["role"] = new_role

            print("Login record updated successfully.")
        else:
            print("Login user not found.")

    # -------------------------
    # SEARCH METHODS
    # -------------------------
    def search_student_by_id(self, student_id):
        start_time = time.time()

        if student_id in self.students:
            result = self.students[student_id]
            print("Student found.")
            result.display_records()
        else:
            result = None
            print("Student not found.")

        end_time = time.time()
        print(f"Search time: {end_time - start_time:.6f} seconds")
        return result

    def search_course_by_id(self, course_id):
        start_time = time.time()

        if course_id in self.courses:
            result = self.courses[course_id]
            print("Course found.")
            result.display_course_details()
        else:
            result = None
            print("Course not found.")

        end_time = time.time()
        print(f"Search time: {end_time - start_time:.6f} seconds")
        return result

    def search_professor_by_email(self, prof_email):
        start_time = time.time()

        if prof_email in self.professors:
            result = self.professors[prof_email]
            print("Professor found.")
            result.prof_details()
        else:
            result = None
            print("Professor not found.")

        end_time = time.time()
        print(f"Search time: {end_time - start_time:.6f} seconds")
        return result

    # -------------------------
    # SORT METHODS
    # -------------------------
    def sort_students_by_name(self, reverse=False):
        start_time = time.time()

        sorted_students = sorted(
            self.students.values(),
            key=lambda student: (student.first_name.lower(), student.last_name.lower()),
            reverse=reverse
        )

        end_time = time.time()
        print(f"Sorting time: {end_time - start_time:.6f} seconds")
        return sorted_students

    def sort_students_by_email(self, reverse=False):
        start_time = time.time()

        sorted_students = sorted(
            self.students.values(),
            key=lambda student: student.email.lower(),
            reverse=reverse
        )

        end_time = time.time()
        print(f"Sorting time: {end_time - start_time:.6f} seconds")
        return sorted_students

    def sort_students_by_average_marks(self, reverse=False):
        start_time = time.time()

        def student_average(student):
            scores = []
            if student.student_id in self.grades.grade_records:
                for course_id in self.grades.grade_records[student.student_id]:
                    marks = self.grades.grade_records[student.student_id][course_id]["marks"]
                    scores.extend(marks.values())
            return statistics.mean(scores) if scores else 0

        sorted_students = sorted(
            self.students.values(),
            key=student_average,
            reverse=reverse
        )

        end_time = time.time()
        print(f"Sorting time: {end_time - start_time:.6f} seconds")
        return sorted_students

    # -------------------------
    # STATISTICS
    # -------------------------
    def calculate_course_average(self, course_id):
        all_scores = []

        for student_id in self.grades.grade_records:
            if course_id in self.grades.grade_records[student_id]:
                marks = self.grades.grade_records[student_id][course_id]["marks"]
                for item in marks:
                    all_scores.append(marks[item])

        if not all_scores:
            print("No marks available for this course.")
            return None

        average_score = statistics.mean(all_scores)
        print(f"Average score for {course_id}: {average_score}")
        return average_score

    def calculate_course_median(self, course_id):
        all_scores = []

        for student_id in self.grades.grade_records:
            if course_id in self.grades.grade_records[student_id]:
                marks = self.grades.grade_records[student_id][course_id]["marks"]
                for item in marks:
                    all_scores.append(marks[item])

        if not all_scores:
            print("No marks available for this course.")
            return None

        median_score = statistics.median(all_scores)
        print(f"Median score for {course_id}: {median_score}")
        return median_score

    # -------------------------
    # REPORTS
    # -------------------------
    def report_by_student(self, student_id):
        if student_id in self.students:
            self.students[student_id].display_records()
            self.grades.show_student_report(student_id)
        else:
            print("Student not found.")

    def report_by_course(self, course_id):
        print(f"REPORT FOR COURSE: {course_id}")
        found = False

        for student_id in self.grades.grade_records:
            if course_id in self.grades.grade_records[student_id]:
                found = True
                student = self.students.get(student_id)
                grade_info = self.grades.grade_records[student_id][course_id]

                if student:
                    print(f"\nStudent: {student.first_name} {student.last_name} ({student.student_id})")
                else:
                    print(f"\nStudent ID: {student_id}")

                print(f"Grade: {grade_info['grade']}")
                print("Marks:")
                for item, score in grade_info["marks"].items():
                    print(f"  {item}: {score}")

        if not found:
            print("No records found for this course.")

    def report_by_professor(self, prof_email):
        if prof_email not in self.professors:
            print("Professor not found.")
            return

        professor = self.professors[prof_email]
        print(f"REPORT FOR PROFESSOR: {professor.prof_name}")

        if not professor.current_courses and not professor.past_courses:
            print("No courses found for this professor.")
            return

        print("Current Courses:")
        for course_id in professor.current_courses:
            print(f"  {course_id}")

        print("Past Courses:")
        for year, courses in professor.past_courses.items():
            print(f"  {year}: {', '.join(courses)}")
            
if __name__ == "__main__":
    system = CheckMyGradeSystem()

    print("\n--- ADDING DATA ---")
    student1 = Student("S101", "Ashritha", "Achutharaman", "ash@example.com", ["C101"])
    student2 = Student("S102", "Meera", "Raman", "meera@example.com", ["C102"])

    course1 = Course("C101", "Python Programming", 3, "Spring", "MW", "10:00", "11:15", "In Person")
    course2 = Course("C102", "Data Structures", 4, "Fall", "TR", "1:00", "2:15", "Online")

    professor1 = Professor(
        "Dr. Rao",
        "rao@university.edu",
        "Associate Professor",
        ["C101"],
        {"2024": ["C100"]}
    )

    login1 = LoginUser("ash@example.com", "Password123", "student")

    system.add_student(student1)
    system.add_student(student2)

    system.add_course(course1)
    system.add_course(course2)

    system.add_professor(professor1)

    system.add_login_user(login1)

    print("\n--- DISPLAY STUDENT ---")
    student1.display_records()

    print("\n--- DISPLAY COURSE ---")
    course1.display_course_details()

    print("\n--- DISPLAY PROFESSOR ---")
    professor1.prof_details()
    professor1.prof_course_details()

    print("\n--- MODIFY STUDENT ---")
    system.modify_student("S101", new_first_name="Asha", new_email="asha@example.com")
    system.search_student_by_id("S101")

    print("\n--- MODIFY COURSE ---")
    system.modify_course("C101", new_course_name="Advanced Python", new_modality="Hybrid")
    system.search_course_by_id("C101")

    print("\n--- MODIFY PROFESSOR ---")
    system.modify_professor("rao@university.edu", new_prof_name="Dr. Raghav Rao")
    system.search_professor_by_email("rao@university.edu")

    print("\n--- ADD GRADE RECORDS ---")
    system.grades.add_course_grade("S101", "C101", "A", {"Quiz": 85, "Midterm": 90, "Final": 95})
    system.grades.add_course_grade("S102", "C101", "B", {"Quiz": 75, "Midterm": 80, "Final": 85})

    print("\n--- SHOW STUDENT REPORT ---")
    system.grades.show_student_report("S101")

    print("\n--- CALCULATE COURSE STATS ---")
    system.calculate_course_average("C101")
    system.calculate_course_median("C101")

    print("\n--- LOGIN TEST ---")
    user = system.login_user("ash@example.com", "Password123")
    if user:
        print("Logged in status:", user.is_logged_in)
        user.logout()

    print("\n--- SAVE TO CSV ---")
    system.save_students_to_csv()
    system.save_courses_to_csv()
    system.save_professors_to_csv()
    system.save_logins_to_csv()
    print("CSV files saved.")

    print("\n--- DELETE TEST ---")
    system.delete_student("S102")
    system.search_student_by_id("S102")