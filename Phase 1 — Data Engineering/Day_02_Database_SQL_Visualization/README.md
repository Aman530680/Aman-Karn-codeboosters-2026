# Day 02 — Database, SQL & Visualization

## Project Objective

This mini project is created using Python, SQLite, Pandas, and Matplotlib to analyze student performance data using SQL queries and create professional visualizations.

The project helps to understand:
- SQL querying using SQLite
- Student performance analysis
- Department wise analysis
- Attendance analysis
- Gender wise analysis
- Top performing students
- Dashboard creation using Matplotlib

---

## Technologies Used

- Python
- Pandas
- SQLite
- Matplotlib
- Seaborn
- VS Code / Google Colab

---

## Project Folder Structure

```text
Day_02_Database_SQL_Visualization
│
├── class_practice2.ipynb
├── Practice_Questions_2.ipynb
├── Student_Performance_Dashboard2.ipynb
├── student_performance.csv
├── Titanic-Dataset.csv
├── student_dashboard.png
└── README.md
```

---

## Files Description

### class_practice2.ipynb
Contains SQLite database setup, SQL query practice, aggregation functions, filtering, grouping, ordering, joins, and visualization examples.

### Practice_Questions_2.ipynb
Contains answers for SQL and visualization practice questions using student and Titanic datasets.

### Student_Performance_Dashboard2.ipynb
Main mini project notebook containing SQL analysis and dashboard creation for student performance data.

### student_performance.csv
Dataset file containing student academic records and attendance details.

### Titanic-Dataset.csv
Dataset used for additional practice questions and SQL operations.

### student_dashboard.png
Final dashboard image generated using Matplotlib.

### README.md
Project documentation file.

---

## Dataset Columns

| Column | Description |
|--------|-------------|
| student_id | Unique student identifier |
| name | Student full name |
| age | Student age |
| gender | Male / Female |
| department | Computer Science, Electronics, Mechanical, Civil |
| semester | Current semester |
| math_score | Math exam score |
| science_score | Science exam score |
| english_score | English exam score |
| programming_score | Programming exam score |
| attendance_percentage | Attendance percentage |
| city | Student's home city |
| admission_year | Year of admission |

---

## Features of the Project

### SQLite Database Operations
- Create SQLite database
- Store CSV data into SQL tables
- Execute SQL queries using Pandas

### SQL Query Practice
- SELECT
- WHERE
- GROUP BY
- HAVING
- ORDER BY
- LIMIT
- Aggregate functions (AVG, COUNT)

### Student Performance Analysis
- Average scores by department
- Student count department wise
- Top performing students
- Attendance analysis
- Gender wise performance analysis

### Visualization
- Bar charts
- Pie charts
- Horizontal bar charts
- Dashboard design using `plt.subplots()`

### Dashboard Features
- Average math score by department
- Student distribution by department
- Top 8 students based on total score
- Average attendance percentage by gender

---

## Key Query Results

### Department Wise Analysis
| Department | Students | Avg Math | Avg Programming | Avg Attendance |
|------------|----------|----------|-----------------|----------------|
| Computer Science | 13 | 85.62 | 89.23 | 90.69% |
| Electronics | 6 | 71.00 | 61.50 | 80.33% |
| Mechanical | 6 | 71.00 | 49.33 | 83.50% |
| Civil | 5 | 63.40 | 40.60 | 74.60% |

### Gender Wise Analysis
| Gender | Students | Avg Math | Avg Programming | Avg Attendance |
|--------|----------|----------|-----------------|----------------|
| Female | 15 | 78.47 | 70.20 | 88.53% |
| Male | 15 | 73.67 | 65.00 | 80.47% |

### Top 5 Students (Total Score)
| Name | Department | Total Score |
|------|------------|-------------|
| Ananya Das | Computer Science | 371 |
| Tanvi Mehta | Computer Science | 367 |
| Akanksha Yadav | Computer Science | 365 |
| Arjun Nair | Computer Science | 356 |
| Divya Singh | Computer Science | 356 |

---

## How to Run the Project

### Step 1
Open the project folder in VS Code

### Step 2
Select the `.venv` Python kernel in the notebook

### Step 3
Import required libraries

```python
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
```

### Step 4
Read the dataset

```python
student_data = pd.read_csv("student_performance.csv")
```

### Step 5
Run all notebook cells

> **Note:** The `google.colab` import cells can be skipped — all CSV files are already in the same folder locally.

---

## Learning Outcomes

Through this project, we learned:
- Working with SQLite databases
- Writing SQL queries in Python
- Data filtering and grouping
- Aggregate functions in SQL
- Using `pd.read_sql_query()`
- Data visualization using Matplotlib
- Creating dashboards using subplots
- Saving charts as images

---

## Author

Aman Karn

Third Year CSE Student  
Sri Eshwar College of Engineering
