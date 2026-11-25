# Student Grade Calculator (Module 02 Mini Project)

A command-line **Student Grade Calculator** built with Python's standard library. It lets you manage student records, compute subject averages, letter grades, and 4.0-scale GPAs, view class-wide statistics, and persist data automatically to JSON.

## Features

- **Add students & subject scores** with input validation (`0`–`100`)
- **Update individual subject scores** for existing students
- **View all students** in a formatted summary table
- **Search student reports** with per-subject breakdown
- **Class summary** showing class average, highest/lowest performers, and grade distribution (`A`–`F`)
- **Automatic JSON persistence** (`grades.json`)
- **Unit tests** using `unittest`

## Grading Scale

| Average | Letter Grade | GPA |
| --- | --- | --- |
| 90 – 100 | A | 4.0 |
| 80 – 89.99 | B | 3.0 |
| 70 – 79.99 | C | 2.0 |
| 60 – 69.99 | D | 1.0 |
| 0 – 59.99 | F | 0.0 |

## Project Structure

```text
module-02-student-grade-calculator/
├── grade_calculator.py       # Core grading logic and GradeBook class
├── main.py                   # Interactive CLI application
├── tests/
│   ├── __init__.py
│   └── test_grade_calculator.py
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+ (no external packages required)

### Run the Application

```bash
python main.py
```

### Run Tests

```bash
python -m unittest discover -s tests -v
```
