# Student Data Explorer

## Project Objective

This mini project is created using Python and Pandas to analyze student performance data and generate useful reports.

The project helps to understand:
- Student performance
- Department wise analysis
- Attendance analysis
- Gender wise analysis
- Top performing students

---

## Technologies Used

- Python
- Pandas
- Google Colab

---

## Project Folder Structure

```text
Day_01_Introduction_to_Data_Engineering
│
├── class_practice.ipynb
├── PRACTICE_QUESTIONS.ipynb
├── Student_Data_Explorer.ipynb
├── student_performance.csv
└── README.md
```

---

## Files Description

### class_practice.ipynb
Contains basic Pandas practice programs and dataset operations.

### PRACTICE_QUESTIONS.ipynb
Contains answers for all practice questions based on the student dataset.

### Student_Data_Explorer.ipynb
Main mini project notebook containing complete student data analysis.

### student_performance.csv
Dataset file containing student details and scores.

### README.md
Project documentation file.

---

## Dataset Columns

- student_id
- name
- age
- gender
- department
- semester
- math_score
- science_score
- english_score
- programming_score
- attendance_percentage
- city
- admission_year

---

## Features of the Project

### Dataset Overview
- Total number of students
- Total number of columns
- Unique departments

### Department Wise Analysis
- Count students department wise

### Score Analysis
- Highest math score
- Lowest math score
- Average math score
- Average programming score
- Average attendance percentage

### Gender Wise Analysis
- Average total score based on gender

### Top 5 Students
- Displays top students based on total score

### Attendance Analysis
- Students with attendance below 75%

### Practice Questions
- Electronics department student count
- Female attendance average
- Lowest programming score
- Students scored above 80 in math
- Average total score for attendance above 90%

---

## How to Run the Project

### Step 1
Open Google Colab

### Step 2
Upload the CSV file

```python
from google.colab import files
uploaded = files.upload()
```

### Step 3
Import pandas

```python
import pandas as pd
```

### Step 4
Read the dataset

```python
student_data = pd.read_csv("student_performance.csv")
```

### Step 5
Run all notebook cells

---

## Learning Outcomes

Through this project, we learned:
- Data analysis using Pandas
- Data filtering
- Grouping data
- Sorting values
- Finding averages and maximum values
- Working with CSV files
- Using DataFrames in Python

---

## Author

Aman Karn

Third Year CSE Student  
Sri Eshwar College of Engineering