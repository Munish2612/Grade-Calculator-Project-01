"""Interactive CLI for the Student Grade Calculator."""

from __future__ import annotations

from pathlib import Path

from grade_calculator import GradeBook


DATA_FILE = Path(__file__).parent / "grades.json"


def prompt_score(prompt_text: str) -> float:
    """Prompt the user until a valid score (0-100) is entered."""
    while True:
        raw = input(prompt_text).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Invalid input. Please enter a numeric score (0-100).")
            continue
        if 0 <= value <= 100:
            return value
        print("Score must be between 0 and 100.")


def handle_add_student(book: GradeBook) -> None:
    """Add a new student and their subject scores."""
    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
        return

    if name in book.students:
        overwrite = input(
            f"'{name}' already exists. Overwrite their record? (y/n): "
        ).strip().lower()
        if overwrite != "y":
            print("Cancelled.")
            return

    scores: dict[str, float] = {}
    print("Enter subjects and scores (leave subject blank when done):")
    while True:
        subject = input("  Subject name: ").strip()
        if not subject:
            break
        scores[subject] = prompt_score(f"  Score for {subject} (0-100): ")

    book.add_student(name, scores)
    book.save()
    print(f"Saved '{name}' with {len(scores)} subject(s).")


def handle_update_score(book: GradeBook) -> None:
    """Add or update a single subject score for an existing student."""
    name = input("Enter student name: ").strip()
    if name not in book.students:
        print(f"Student '{name}' not found.")
        return

    subject = input("Enter subject name: ").strip()
    if not subject:
        print("Subject name cannot be empty.")
        return

    score = prompt_score(f"Enter score for {subject} (0-100): ")
    book.set_score(name, subject, score)
    book.save()
    print(f"Updated {name}'s {subject} score to {score:.2f}.")


def print_student_report(report: dict) -> None:
    """Pretty-print a single student's report."""
    print(f"\nStudent: {report['name']}")
    if not report["scores"]:
        print("  No scores recorded yet.")
        return
    for subject, score in report["scores"].items():
        print(f"  - {subject}: {score:.2f}")
    print(
        f"  Average: {report['average']:.2f} | "
        f"Grade: {report['letter_grade']} | "
        f"GPA: {report['gpa']:.1f}"
    )


def handle_view_all(book: GradeBook) -> None:
    """Display a formatted table of all students."""
    reports = book.get_all_reports()
    if not reports:
        print("No students recorded yet.")
        return

    print("\n" + "-" * 62)
    print(f"{'Student':<22} {'Subjects':>8} {'Average':>10} {'Grade':>8} {'GPA':>8}")
    print("-" * 62)
    for r in reports:
        print(
            f"{r['name']:<22} {len(r['scores']):>8} "
            f"{r['average']:>10.2f} {r['letter_grade']:>8} {r['gpa']:>8.1f}"
        )
    print("-" * 62)


def handle_search_student(book: GradeBook) -> None:
    """Search for a student by exact name (case-insensitive fallback)."""
    query = input("Enter student name to search: ").strip()
    if not query:
        print("Please enter a name.")
        return

    if query in book.students:
        print_student_report(book.get_student_report(query))
        return

    matches = [
        name for name in book.students if query.lower() in name.lower()
    ]
    if not matches:
        print(f"No student matching '{query}' found.")
        return

    for match in sorted(matches):
        print_student_report(book.get_student_report(match))


def handle_class_summary(book: GradeBook) -> None:
    """Display class-wide statistics and grade distribution."""
    summary = book.get_class_summary()
    print("\n=== Class Summary ===")
    print(f"Total students : {summary['total_students']}")
    print(f"Graded students: {summary['graded_students']}")
    if summary["graded_students"] == 0:
        print("No graded students yet.")
        return

    print(f"Class average  : {summary['class_average']:.2f}")
    high = summary["highest"]
    low = summary["lowest"]
    print(f"Highest        : {high['name']} ({high['average']:.2f})")
    print(f"Lowest         : {low['name']} ({low['average']:.2f})")
    dist = summary["distribution"]
    dist_str = " | ".join(f"{grade}: {count}" for grade, count in dist.items())
    print(f"Distribution   : {dist_str}")


def handle_delete_student(book: GradeBook) -> None:
    """Remove a student from the gradebook."""
    name = input("Enter student name to delete: ").strip()
    if book.remove_student(name):
        book.save()
        print(f"Removed '{name}'.")
    else:
        print(f"Student '{name}' not found.")


def print_menu() -> None:
    """Print the main CLI menu."""
    print("\n=== Student Grade Calculator ===")
    print("1. Add student & scores")
    print("2. Add / update a subject score")
    print("3. View all students")
    print("4. Search student report")
    print("5. View class summary")
    print("6. Delete student")
    print("7. Exit")


def main() -> None:
    """Run the interactive Student Grade Calculator loop."""
    book = GradeBook(DATA_FILE)
    book.load()

    actions = {
        "1": handle_add_student,
        "2": handle_update_score,
        "3": handle_view_all,
        "4": handle_search_student,
        "5": handle_class_summary,
        "6": handle_delete_student,
    }

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            book.save()
            print("Grades saved. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(book)
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
