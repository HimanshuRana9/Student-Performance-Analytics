# Student Performance Analytics System

An academic data analytics project built with **Python**, **Pandas**, and **NumPy** to evaluate, process, and analyze student academic performance from raw CSV data.

---

## 📌 Project Description

The **Student Performance Analytics System** is a modular, console-based analytical tool designed for Python with AI students. It provides automated ingestion, validation, and statistical analysis of student academic records. The system computes individual metrics (total marks, percentage averages, academic grades, and pass/fail statuses) alongside macro-level insights including class averages, subject-wise comparisons, top performers, attendance trends, and department-level aggregations.

This project strictly adheres to academic Python and data analysis principles—avoiding machine learning, web frameworks, and external databases in favor of transparent, clean, and well-structured code.

---

## 🎯 Objectives

- Demonstrate practical proficiency in Python fundamentals (variables, data types, conditions, loops, and functions).
- Utilize **Pandas** for structured CSV data loading, DataFrame manipulation, filtering, grouping, and aggregations.
- Apply **NumPy** for vector operations, mathematical statistics (mean, median, min, max, standard deviation), and array indexing.
- Implement robust data validation and defensive error handling for reliable pipeline execution.
- Deliver clear, well-formatted console reporting and actionable educational insights.

---

## 🛠️ Technologies Used

- **Python 3.14+**: Core programming language.
- **Pandas**: Structured data management, DataFrame operations, grouping, and aggregations.
- **NumPy**: Vectorized arithmetic, array-level processing, and descriptive statistical calculations.

---

## 📊 Dataset

The project processes a structured student performance dataset stored in `students.csv`.

- **Total Records**: 30 student entries
- **Attributes**:
  1. `student_id`: Unique identifier for each student (Integer)
  2. `name`: Student's name (String)
  3. `department`: Academic department (`CSE`, `AIML`, `ECE`, `ISE`)
  4. `year`: Year of study (1 to 4)
  5. `age`: Age in years (18 to 22)
  6. `attendance`: Attendance percentage (66% to 96%)
  7. `python_marks`: Marks scored in Python (61 to 97, out of 100)
  8. `ml_marks`: Marks scored in Machine Learning (65 to 98, out of 100)
  9. `projects_completed`: Number of hands-on projects finished (1 to 5)

---

## 🚀 Key Features

1. **Automated CSV Ingestion & Validation**:
   - Safe file reading with handling for `FileNotFoundError` and empty datasets.
   - Rigorous schema checks (column presence, numeric types, and sensible 0–100 ranges).
2. **Student Metric Calculations**:
   - **Total Marks**: Vectorized sum of Python Marks + ML Marks.
   - **Average Marks**: Mean score calculated programmatically and rounded to 2 decimal places.
3. **Academic Grading System**:
   - Automated letter grade assignment (`A+`, `A`, `B`, `C`, `D`, `E`, `F`) using strict boundary criteria.
4. **Subject-Level Pass/Fail Logic**:
   - Ensures students achieve both subject-level minimums and class average thresholds.
5. **Statistical Analysis with NumPy**:
   - Subject-wise metrics (average, highest, lowest, median, standard deviation).
   - Identification of best and weakest performing subjects.
6. **Cohort & Class Performance**:
   - Overall class average, highest/lowest scores, pass count, and pass percentage.
7. **Top Performers Leaderboard**:
   - Ranked display of top-performing students sorted by average marks with attendance tie-breaking.
8. **Attendance Analysis**:
   - Average, peak, and low attendance figures, identification of students below 75% attendance, and correlation analysis.
9. **Department-Wise Performance**:
   - Group-by analysis summarizing student counts, subject averages, and overall departmental averages.
10. **Actionable Educational Insights**:
    - Factual, data-derived conclusions printed directly to the console.

---

## 📏 Academic Rules

### 1. Grading Rule

Grades are assigned based on the student's calculated `average_marks`:

| Average Marks Range | Grade | Description |
| :------------------ | :---: | :---------- |
| **90.0% – 100.0%**  |  A+   | Outstanding |
| **80.0% – 89.99%**  |   A   | Excellent   |
| **70.0% – 79.99%**  |   B   | Good        |
| **60.0% – 69.99%**  |   C   | Average     |
| **50.0% – 59.99%**  |   D   | Below Avg   |
| **40.0% – 49.99%**  |   E   | Marginal    |
| **Below 40.0%**     |   F   | Fail        |

### 2. Pass / Fail Rule

A student is awarded a **"Pass"** result if and only if **both** of the following criteria are met:
1. `average_marks >= 40.0`
2. Every subject mark (`python_marks >= 33.0` and `ml_marks >= 33.0`)

If any subject mark falls below 33 or the average marks fall below 40, the student is marked as **"Fail"**.

---

## 📁 Project Structure

```text
Student-Performance-Analytics/
│
├── main.py                     # Main application entry point orchestrating the analytics pipeline
├── functions.py                # Reusable, modular functions for loading, validation, and analytics
├── students.csv                # Primary student dataset (30 records, 9 attributes)
├── requirements.txt            # Minimal Python dependencies (pandas, numpy)
├── README.md                   # Project overview, instructions, rules, and documentation
├── Project_Documentation.md    # Detailed academic technical report
├── .gitignore                  # Git ignore rules for Python artifacts and caches
└── screenshots/                # Execution logs and screenshot evidence
    ├── terminal_output.png     # High-resolution visual terminal capture
    ├── terminal_output.txt     # Raw execution output log from main.py
    └── README.md               # Screenshot manifest and capture guide
```

---

## 💻 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/HimanshuRana9/Student-Performance-Analytics.git
cd Student-Performance-Analytics
```

### 2. Install Required Dependencies
Ensure you have Python 3 installed, then install `pandas` and `numpy`:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Execute `main.py` from your terminal:
```bash
python main.py
```

---

## 🖥️ Sample Console Output

```text
========================================================================================
                          STUDENT PERFORMANCE ANALYTICS SYSTEM                          
========================================================================================

DATASET OVERVIEW
----------------------------------------------------------------------------------------
Total Student Records : 30
Total Attributes      : 13
Attributes Included   : student_id, name, department, year, age, attendance, python_marks, ml_marks, projects_completed, total_marks, average_marks, grade, result
Validation Status     : Passed (No missing/corrupt values)

CLASS PERFORMANCE
----------------------------------------------------------------------------------------
Total Students Enrolled : 30
Overall Class Average   : 82.35%
Highest Average Score   : 97.50% (Sanya, AIML)
Lowest Average Score    : 63.00% (Manish, CSE)
Students Passed         : 30
Students Failed         : 0
Overall Pass Percentage : 100.00%

SUBJECT-WISE PERFORMANCE
----------------------------------------------------------------------------------------
[Python]
  Average Score   : 81.40
  Highest Score   : 97
  Lowest Score    : 61
  Median Score    : 82.50
  Std Deviation   : 10.08
[Machine Learning]
  Average Score   : 83.30
  Highest Score   : 98
  Lowest Score    : 65
  Median Score    : 84.00
  Std Deviation   : 9.37

Best Performing Subject   : Machine Learning (Average: 83.30)
Weakest Performing Subject: Python (Average: 81.40)

TOP PERFORMERS (TOP 5 STUDENTS)
----------------------------------------------------------------------------------------
Rank   Student ID   Name           Department      Average   Grade    Result 
---------------------------------------------------------------------------
#1     22           Sanya          AIML             97.50%    A+       Pass  
#2     29           Nikhil         AIML             96.50%    A+       Pass  
#3     19           Varun          CSE              94.50%    A+       Pass  
#4     11           Rahul          AIML             94.50%    A+       Pass  
#5     2            Ananya         AIML             92.50%    A+       Pass  
---------------------------------------------------------------------------

DEPARTMENT-WISE PERFORMANCE
----------------------------------------------------------------------------------------
Department     Students    Avg Python        Avg ML    Avg Overall   Avg Attendance
------------------------------------------------------------------------------------
AIML                  9         90.89         93.22         92.06%           86.67%
ECE                   6         79.83         79.50         79.67%           85.50%
ISE                   5         76.60         79.80         78.20%           78.80%
CSE                  10         76.20         78.40         77.30%           79.10%
------------------------------------------------------------------------------------
```

*(Full log available in `screenshots/terminal_output.txt`)*

---

## 🧠 Learning Outcomes

- **Python Fundamentals**: Hands-on application of data structures (lists, dictionaries), control flow (`if/elif/else`), iteration (`for` loops), and modular programming with custom functions.
- **Data Analysis with Pandas**: Loading tabular CSV data, data cleansing and validation, adding calculated Series, sorting, and aggregate summarization via `groupby()`.
- **Numerical Computing with NumPy**: Applying vectorized operations (`np.add`, `np.divide`), computing statistical metrics (`np.mean`, `np.median`, `np.std`, `np.max`, `np.min`), and array indexing.
- **Software Engineering Best Practices**: Separation of concerns (`main.py` vs `functions.py`), comprehensive exception handling, clean code formatting, and Git version control.

---

## 👤 Author

- **Himanshu Rana** ([HimanshuRana9](https://github.com/HimanshuRana9))
- Academic Project for **Python with AI**
