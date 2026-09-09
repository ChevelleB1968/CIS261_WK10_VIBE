# Chevelle Brown
# CIS261
# VIBE Coding

"""Manage student records, test scores, and calculated grades."""

from dataclasses import dataclass


@dataclass
class Student:
	"""Store one student's identifying information and test scores."""

	student_id: str
	name: str
	test1: float
	test2: float
	test3: float

	@property
	def average(self) -> float:
		return (self.test1 + self.test2 + self.test3) / 3

	@property
	def grade(self) -> str:
		average = self.average
		if average >= 90:
			return "A"
		if average >= 80:
			return "B"
		if average >= 70:
			return "C"
		if average >= 60:
			return "D"
		return "F"

	@property
	def letter_grade(self) -> str:
		return self.grade


def read_score(prompt: str = "Enter a test score (0-100): ") -> float:
	"""Read a score and continue prompting until it is valid."""
	while True:
		try:
			score = float(input(prompt))
		except ValueError:
			print("Please enter a number from 0 to 100.")
			continue
		if 0 <= score <= 100:
			return score
		print("Please enter a number from 0 to 100.")


def add_student(students: dict[str, Student]) -> None:
	student_id = input("Student ID: ").strip()
	if not student_id:
		print("Student ID cannot be empty.")
		return
	if student_id in students:
		print("That student ID already exists.")
		return

	name = input("Student name: ").strip()
	if not name:
		print("Student name cannot be empty.")
		return

	test1 = read_score("Test 1 score (0-100): ")
	test2 = read_score("Test 2 score (0-100): ")
	test3 = read_score("Test 3 score (0-100): ")
	student = Student(student_id, name, test1, test2, test3)
	students[student_id] = student
	print(f"Added {student.name} with a {student.average:.2f}% ({student.letter_grade}).")


def add_score(students: dict[str, Student]) -> None:
	student_id = input("Student ID: ").strip()
	student = students.get(student_id)
	if student is None:
		print("Student not found.")
		return
	test_number = input("Which test should be updated (1, 2, or 3)? ").strip()
	if test_number not in {"1", "2", "3"}:
		print("Please choose test 1, 2, or 3.")
		return
	score = read_score(f"Test {test_number} score (0-100): ")
	if test_number == "1":
		student.test1 = score
	elif test_number == "2":
		student.test2 = score
	else:
		student.test3 = score
	print(f"Updated average: {student.average:.2f}% ({student.letter_grade}).")


def display_student(student: Student) -> None:
	print(
		f"{student.student_id} | {student.name} | "
		f"Test 1: {student.test1:.2f}, Test 2: {student.test2:.2f}, "
		f"Test 3: {student.test3:.2f} | "
		f"Average: {student.average:.2f}% | Grade: {student.letter_grade}"
	)


def view_student(students: dict[str, Student]) -> None:
	student_id = input("Student ID: ").strip()
	student = students.get(student_id)
	if student is None:
		print("Student not found.")
		return
	display_student(student)


def search_by_name(students: dict[str, Student]) -> None:
	search_name = input("Enter a name to search for: ").strip().lower()
	if not search_name:
		print("Search name cannot be empty.")
		return

	matches = [
		student
		for student in students.values()
		if search_name in student.name.lower()
	]
	if not matches:
		print("No students found with that name.")
		return

	print("\nMatching Students")
	print("-" * 80)
	for student in sorted(matches, key=lambda item: item.name.lower()):
		display_student(student)


def view_all_students(students: dict[str, Student]) -> None:
	if not students:
		students.update(load_records())
	if not students:
		print("No student records are available. Add a student or load student_grades.txt.")
		return
	print("\nStudent Records")
	header = (
		f"{'ID':<12} {'Name':<24} {'Test 1':>8} {'Test 2':>8} "
		f"{'Test 3':>8} {'Average':>9} {'Grade':>6}"
	)
	print(header)
	print("-" * len(header))
	for student in sorted(students.values(), key=lambda item: item.name.lower()):
		print(
			f"{student.student_id:<12} {student.name:<24} "
			f"{student.test1:>8.2f} {student.test2:>8.2f} "
			f"{student.test3:>8.2f} {student.average:>9.2f} "
			f"{student.letter_grade:>6}"
		)


def view_class_statistics(students: dict[str, Student]) -> None:
	if not students:
		print("No student records have been added.")
		return

	student_list = list(students.values())
	highest = max(student_list, key=lambda student: student.average)
	lowest = min(student_list, key=lambda student: student.average)
	class_average = sum(student.average for student in student_list) / len(student_list)

	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f}% ({highest.name})")
	print(f"Lowest average: {lowest.average:.2f}% ({lowest.name})")
	print(f"Class average: {class_average:.2f}%")


def load_records() -> dict[str, Student]:
	students: dict[str, Student] = {}
	try:
		with open("student_grades.txt", "r", encoding="utf-8") as file:
			for line in file:
				line = line.strip()
				if not line or line == "name|id|test1|test2|test3|average|grade":
					continue
				fields = line.split("|")
				if len(fields) != 7:
					continue
				try:
					student = Student(
						fields[1],
						fields[0],
						float(fields[2]),
						float(fields[3]),
						float(fields[4]),
					)
				except ValueError:
					continue
				students[student.student_id] = student
	except FileNotFoundError:
		return students
	except (OSError, UnicodeError) as error:
		print(f"Could not load student records: {error}")
	return students


def save_records(students: dict[str, Student]) -> None:
	try:
		with open("student_grades.txt", "w", encoding="utf-8") as file:
			file.write("name|id|test1|test2|test3|average|grade\n")
			for student in sorted(students.values(), key=lambda item: item.name.lower()):
				file.write(
					f"{student.name}|{student.student_id}|{student.test1:.2f}|"
					f"{student.test2:.2f}|{student.test3:.2f}|"
					f"{student.average:.2f}|{student.grade}\n"
				)
	except (OSError, UnicodeError) as error:
		print(f"Could not save student records: {error}")
		return
	print(f"Saved {len(students)} student record(s) to student_grades.txt.")


def print_menu() -> None:
	print("\nStudent Record Manager")
	print("1. Add a student")
	print("2. Add a test score")
	print("3. View one student")
	print("4. View all students")
	print("5. View class statistics")
	print("6. Search by student name")
	print("7. Save records to file")
	print("Press ESC to exit")


def main() -> None:
	students = load_records()
	if students:
		print(f"Loaded {len(students)} student record(s) from student_grades.txt.")
	actions = {
		"1": add_student,
		"2": add_score,
		"3": view_student,
		"4": view_all_students,
		"5": view_class_statistics,
		"6": search_by_name,
		"7": save_records,
	}

	while True:
		print_menu()
		choice = input("Choose an option: ").strip()
		if choice == "\x1b":
			print("Goodbye!")
			break
		action = actions.get(choice)
		if action is None:
			print("Please choose an option from 1 to 7, or press ESC to exit.")
			continue
		action(students)


if __name__ == "__main__":
	main()
