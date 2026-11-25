"""Unit tests for the Student Grade Calculator."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from grade_calculator import (
    GradeBook,
    calculate_average,
    get_gpa,
    get_letter_grade,
    validate_score,
)


class TestGradeHelpers(unittest.TestCase):
    def test_validate_score_valid(self) -> None:
        self.assertEqual(validate_score(0), 0.0)
        self.assertEqual(validate_score(85.5), 85.5)
        self.assertEqual(validate_score(100), 100.0)

    def test_validate_score_invalid(self) -> None:
        for bad in (-1, 100.1, "90", True):
            with self.assertRaises(ValueError):
                validate_score(bad)  # type: ignore[arg-type]

    def test_calculate_average(self) -> None:
        self.assertEqual(calculate_average([]), 0.0)
        self.assertEqual(calculate_average([80, 90, 100]), 90.0)
        self.assertEqual(calculate_average([85, 92, 78]), 85.0)

    def test_letter_grade_and_gpa_boundaries(self) -> None:
        cases = [
            (95.0, "A", 4.0),
            (90.0, "A", 4.0),
            (89.99, "B", 3.0),
            (80.0, "B", 3.0),
            (75.0, "C", 2.0),
            (65.0, "D", 1.0),
            (59.99, "F", 0.0),
        ]
        for avg, expected_letter, expected_gpa in cases:
            self.assertEqual(get_letter_grade(avg), expected_letter)
            self.assertEqual(get_gpa(avg), expected_gpa)


class TestGradeBook(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "grades.json"
        self.book = GradeBook(self.data_file)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_report_student(self) -> None:
        self.book.add_student("Alice", {"Math": 92, "Science": 88})
        report = self.book.get_student_report("Alice")
        self.assertEqual(report["average"], 90.0)
        self.assertEqual(report["letter_grade"], "A")
        self.assertEqual(report["gpa"], 4.0)

    def test_set_score_and_remove_student(self) -> None:
        self.book.add_student("Bob", {"Math": 70})
        self.book.set_score("Bob", "English", 80)
        self.assertEqual(self.book.get_student_report("Bob")["average"], 75.0)
        self.assertTrue(self.book.remove_student("Bob"))
        self.assertFalse(self.book.remove_student("Bob"))

    def test_class_summary(self) -> None:
        self.book.add_student("Alice", {"Math": 95})
        self.book.add_student("Bob", {"Math": 75})
        self.book.add_student("Charlie", {})
        summary = self.book.get_class_summary()
        self.assertEqual(summary["total_students"], 3)
        self.assertEqual(summary["graded_students"], 2)
        self.assertEqual(summary["class_average"], 85.0)
        self.assertEqual(summary["highest"]["name"], "Alice")
        self.assertEqual(summary["lowest"]["name"], "Bob")
        self.assertEqual(summary["distribution"]["A"], 1)
        self.assertEqual(summary["distribution"]["C"], 1)

    def test_save_and_load(self) -> None:
        self.book.add_student("Alice", {"Math": 91.5, "History": 84.0})
        self.book.save()

        reloaded = GradeBook(self.data_file)
        reloaded.load()
        report = reloaded.get_student_report("Alice")
        self.assertEqual(report["scores"], {"Math": 91.5, "History": 84.0})
        self.assertEqual(report["average"], 87.75)
        self.assertEqual(report["letter_grade"], "B")


if __name__ == "__main__":
    unittest.main()
