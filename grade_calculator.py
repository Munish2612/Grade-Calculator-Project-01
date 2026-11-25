"""Core logic for the Student Grade Calculator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


GRADE_SCALE: list[tuple[float, str, float]] = [
    (90.0, "A", 4.0),
    (80.0, "B", 3.0),
    (70.0, "C", 2.0),
    (60.0, "D", 1.0),
    (0.0, "F", 0.0),
]


def validate_score(score: float) -> float:
    """Validate that a numeric score is between 0 and 100 inclusive."""
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        raise ValueError("Score must be a number.")
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")
    return float(score)


def calculate_average(scores: list[float]) -> float:
    """Return the arithmetic mean of a list of scores, or 0.0 if empty."""
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def get_letter_grade(average: float) -> str:
    """Map a numeric average (0-100) to a letter grade."""
    for threshold, letter, _ in GRADE_SCALE:
        if average >= threshold:
            return letter
    return "F"


def get_gpa(average: float) -> float:
    """Map a numeric average (0-100) to a 4.0-scale GPA."""
    for threshold, _, gpa in GRADE_SCALE:
        if average >= threshold:
            return gpa
    return 0.0


class GradeBook:
    """Manages student records, subject scores, and class statistics."""

    def __init__(self, data_file: str | Path = "grades.json") -> None:
        self.data_file = Path(data_file)
        self.students: dict[str, dict[str, float]] = {}

    def add_student(self, name: str, scores: dict[str, float] | None = None) -> None:
        """Add a new student or overwrite/initialize their record."""
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Student name cannot be empty.")
        validated: dict[str, float] = {}
        if scores:
            for subject, score in scores.items():
                subj = subject.strip()
                if not subj:
                    raise ValueError("Subject name cannot be empty.")
                validated[subj] = validate_score(score)
        self.students[clean_name] = validated

    def set_score(self, name: str, subject: str, score: float) -> None:
        """Add or update a subject score for an existing student."""
        clean_name = name.strip()
        clean_subject = subject.strip()
        if clean_name not in self.students:
            raise KeyError(f"Student '{clean_name}' not found.")
        if not clean_subject:
            raise ValueError("Subject name cannot be empty.")
        self.students[clean_name][clean_subject] = validate_score(score)

    def remove_student(self, name: str) -> bool:
        """Remove a student by name. Returns True if removed, False if not found."""
        clean_name = name.strip()
        if clean_name in self.students:
            del self.students[clean_name]
            return True
        return False

    def get_student_report(self, name: str) -> dict[str, Any]:
        """Return a summary dict with scores, average, letter grade, and GPA."""
        clean_name = name.strip()
        if clean_name not in self.students:
            raise KeyError(f"Student '{clean_name}' not found.")
        scores = self.students[clean_name]
        avg = calculate_average(list(scores.values()))
        return {
            "name": clean_name,
            "scores": dict(scores),
            "average": avg,
            "letter_grade": get_letter_grade(avg) if scores else "N/A",
            "gpa": get_gpa(avg) if scores else 0.0,
        }

    def get_all_reports(self) -> list[dict[str, Any]]:
        """Return reports for all students sorted alphabetically by name."""
        return [self.get_student_report(name) for name in sorted(self.students)]

    def get_class_summary(self) -> dict[str, Any]:
        """Compute class-wide average, top/lowest student, and grade distribution."""
        reports = [r for r in self.get_all_reports() if r["scores"]]
        if not reports:
            return {
                "total_students": len(self.students),
                "graded_students": 0,
                "class_average": 0.0,
                "highest": None,
                "lowest": None,
                "distribution": {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0},
            }

        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for report in reports:
            distribution[report["letter_grade"]] += 1

        highest = max(reports, key=lambda r: r["average"])
        lowest = min(reports, key=lambda r: r["average"])
        class_avg = calculate_average([r["average"] for r in reports])

        return {
            "total_students": len(self.students),
            "graded_students": len(reports),
            "class_average": class_avg,
            "highest": {"name": highest["name"], "average": highest["average"]},
            "lowest": {"name": lowest["name"], "average": lowest["average"]},
            "distribution": distribution,
        }

    def save(self) -> None:
        """Persist student records to the JSON data file."""
        self.data_file.write_text(
            json.dumps(self.students, indent=2), encoding="utf-8"
        )

    def load(self) -> None:
        """Load student records from the JSON data file if it exists."""
        if not self.data_file.exists():
            return
        raw = json.loads(self.data_file.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            self.students = {
                str(name): {str(subj): float(val) for subj, val in scores.items()}
                for name, scores in raw.items()
            }
