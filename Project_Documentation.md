# Student Performance Analytics System

---

## 1. Project Title
**Student Performance Analytics System**  
*Academic Project for Python with AI Students*  
*Submission Deadline: 15 October 2026*

---

## 2. Objective
The primary objective of this project is to develop, test, and document an automated, console-based academic analytics system that evaluates student performance data using **Python**, **Pandas**, and **NumPy**. The project provides educational institutions and instructors with actionable insights into:
- Individual student metrics (total marks, overall percentage, letter grades, and pass/fail statuses).
- Cohort and class-level performance benchmarks (overall class average, highest/lowest scores, pass rates).
- Comparative subject analysis (identifying best performing vs. weakest subjects).
- Attendance monitoring and its relationship to academic performance.
- Departmental comparative analysis across computer science and engineering disciplines.

The system is developed with a strict focus on clean, transparent, and reproducible programming—avoiding machine learning models or complex web frameworks in favor of core analytical computing.

---

## 3. Technologies Used
- **Python (v3.14+)**: Chosen as the primary programming language for its readability, strong standard library, and robust data science ecosystem.
- **Pandas (v3.0.5+)**: Utilized for tabular data structures (`DataFrame`, `Series`), CSV data ingestion, schema validation, filtering, sorting, and multi-field aggregations (`groupby`).
- **NumPy (v2.5.1+)**: Utilized for vectorized mathematical operations (array addition, division), fast boolean masking, and descriptive statistics (`mean`, `median`, `std`, `max`, `min`).
- **Git & GitHub**: Version control system and remote repository hosting (`https://github.com/HimanshuRana9/Student-Performance-Analytics.git`).

---

## 4. Dataset Description
The system analyzes student records stored in `students.csv`.

- **Total Observations (Rows)**: 30 students
- **Total Input Attributes (Columns)**: 9 fields

### Attribute Schema
| Field Name | Data Type | Value Range / Categories | Description |
| :--- | :---: | :---: | :--- |
| `student_id` | Integer | 1 to 30 | Unique numeric identifier for each student |
| `name` | String | Alphabetical | First name of the student |
| `department` | String | `AIML`, `CSE`, `ECE`, `ISE` | Enrolled academic department |
| `year` | Integer | 1 to 4 | Current academic study year |
| `age` | Integer | 18 to 22 | Age of the student in years |
| `attendance` | Integer | 66 to 96 (%) | Percentage of attended lecture sessions |
| `python_marks` | Integer | 61 to 97 (out of 100) | Marks secured in Python subject examination |
| `ml_marks` | Integer | 65 to 98 (out of 100) | Marks secured in Machine Learning subject examination |
| `projects_completed` | Integer | 1 to 5 | Number of course projects completed |

### Data Quality & Integrity Audit
An automated initial audit confirmed:
- **Null / Missing Values**: 0 missing values across all 9 columns.
- **Duplicate Records**: 0 duplicate student records.
- **Numerical Validity**: All marks and attendance percentages strictly satisfy $0 \le x \le 100$.

---

## 5. Implementation

The architecture follows modular separation of concerns between `main.py` and `functions.py`.

```
                  ┌──────────────────────┐
                  │     students.csv     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ load_student_data()  │ (pandas.read_csv + error handling)
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │validate_student_data │ (schema & range checks)
                  └──────────┬───────────┘
                             │
                             ▼
               ┌─────────────────────────────┐
               │  calculate_student_metrics  │ (NumPy addition, division,
               └─────────────┬───────────────┘  grading, pass/fail loops)
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      ▼                      ▼                      ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│ Subject-wise │     │  Class-wide  │     │ Department-level │
│  Statistics  │     │  Statistics  │     │   Aggregation    │
│ (NumPy stats)│     │(Min/Max/Avg) │     │ (Pandas groupby) │
└──────┬───────┘     └──────┬───────┘     └────────┬─────────┘
       │                    │                      │
       └────────────────────┼──────────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │     main.py Orchestrator    │
              │  (Formatted Console Output) │
              └─────────────────────────────┘
```

### A. CSV Data Loading (`functions.py -> load_student_data`)
Uses `pd.read_csv()` wrapped in defensive `try-except` blocks to handle:
- Missing file (`FileNotFoundError`)
- Empty files (`pd.errors.EmptyDataError`)
- Generic parsing exceptions

### B. Data Validation (`functions.py -> validate_student_data`)
Ensures data health prior to downstream analytics:
- Verifies that all required column names exist.
- Confirms absence of null values in critical fields (`student_id`, `name`, `department`, `attendance`, `python_marks`, `ml_marks`).
- Validates data types using `pd.api.types.is_numeric_dtype`.
- Performs range checking with NumPy vectorized comparison: `np.any(marks_attendance < 0) or np.any(marks_attendance > 100)`.

### C. NumPy Calculations & Metric Processing (`calculate_student_metrics`)
- **Total Marks**: Vectorized addition using `np.add(python_arr, ml_arr)`.
- **Average Marks**: Vectorized division using `np.divide(total_arr, 2.0)` followed by `np.round()`.
- **Descriptive Statistics**: Evaluates `np.mean()`, `np.median()`, `np.std()`, `np.max()`, and `np.min()` across arrays.

### D. Iteration and Control Flow (Loops & Conditions)
- Row-level iteration via `for` loops assigns academic grades and checks pass/fail conditions for each student individually.
- Subject-level iteration evaluates descriptive statistics across dynamic subject lists.
- Departmental data formatting traverses aggregated summary rows to build aligned console tables.

### E. Academic Rules Implementation

#### 1. Grading Rule
Grades are assigned based on the student's calculated `average_marks`:

$$\text{Grade} = \begin{cases} 
\text{A+} & \text{if } \text{Average Marks} \ge 90.0 \\
\text{A}  & \text{if } 80.0 \le \text{Average Marks} < 90.0 \\
\text{B}  & \text{if } 70.0 \le \text{Average Marks} < 80.0 \\
\text{C}  & \text{if } 60.0 \le \text{Average Marks} < 70.0 \\
\text{D}  & \text{if } 50.0 \le \text{Average Marks} < 60.0 \\
\text{E}  & \text{if } 40.0 \le \text{Average Marks} < 50.0 \\
\text{F}  & \text{if } \text{Average Marks} < 40.0 
\end{cases}$$

#### 2. Pass / Fail Rule
To ensure comprehensive academic proficiency, passing requires satisfying **both** an aggregate threshold and individual subject standards:

$$\text{Result} = \begin{cases} 
\text{Pass} & \text{if } (\text{Average Marks} \ge 40.0) \land (\text{Python Marks} \ge 33.0) \land (\text{ML Marks} \ge 33.0) \\
\text{Fail} & \text{otherwise}
\end{cases}$$

This prevents a student who scores exceptionally high in one subject from passing if they fail another.

---

## 6. Key Features
1. **Modular Architecture**: Reusable analytical functions isolated in `functions.py` with complete docstrings.
2. **Defensive Error Handling**: Clear, user-friendly error diagnostics preventing unhandled application crashes.
3. **Double Verification**: Numerical calculations conducted via vectorized operations and cross-verified against iterative logic.
4. **Comprehensive Console Dashboard**: Formatted ASCII table presentations of individual results and macro statistics.
5. **Multi-Disciplinary Grouping**: Group-by department summarization for comparative academic evaluations.
6. **Attendance Correlation Analysis**: Evaluates Pearson correlation between class attendance and performance.

---

## 7. Output / Screenshots

The system produces a structured, readable terminal output. All evidence is archived inside the `screenshots/` directory:
- `screenshots/terminal_output.png`: High-resolution terminal capture of the entire execution.
- `screenshots/terminal_output.txt`: Raw console output log.
- `screenshots/README.md`: Screenshot manifest and manual capture guide.

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

STUDENT PERFORMANCE SUMMARY
----------------------------------------------------------------------------------------
ID    Name       Department   Attendance   Python     ML   Total   Average  Grade   Result 
----------------------------------------------------------------------------------------
1     Aarav      CSE                 82%       78     81     159     79.50    B      Pass  
2     Ananya     AIML                91%       91     94     185     92.50   A+      Pass  
3     Arjun      CSE                 76%       67     72     139     69.50    C      Pass  
4     Diya       ECE                 88%       82     79     161     80.50    A      Pass  
5     Rohan      AIML                69%       88     91     179     89.50    A      Pass  
... (all 30 students displayed)
----------------------------------------------------------------------------------------

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

---

## 8. Final Outcome
The system successfully processes all 30 student records and computes the following verified analytical metrics:

### Summary of Verified Results
- **Cohort Size**: 30 students
- **Class Average**: **82.35%**
- **Top Performer**: Sanya (ID: 22, AIML) with **97.50%** (Grade A+)
- **Lowest Performer**: Manish (ID: 21, CSE) with **63.00%** (Grade C)
- **Subject Averages**: Machine Learning **83.30%**, Python **81.40%**
- **Best Subject**: Machine Learning
- **Weakest Subject**: Python
- **Pass / Fail**: 30 Passed, 0 Failed (**100.00% Pass Rate**)
- **Attendance Average**: **82.60%** (Peak: 96.00% by Sanya; Lowest: 66.00% by Meera)
- **Students with < 75% Attendance**: 7 students
- **Attendance-Marks Association**: +0.754 correlation (positive association observed)
- **Top Performing Department**: AIML with **92.06%** overall average

---

## 9. Challenges & Learning
1. **Defensive Data Ingestion**:
   - *Challenge*: Real-world datasets often present missing values, unexpected column names, or out-of-bounds numbers.
   - *Learning*: Implemented a dedicated validation layer in `functions.py` that confirms schema integrity and value bounds before any mathematical calculations occur.
2. **Balancing Loops with Vectorization**:
   - *Challenge*: Academic assignments require demonstrating both procedural iteration (`for` loops) and vectorized performance (`pandas`/`numpy`).
   - *Learning*: Used NumPy for high-throughput arithmetic operations (array sum, array mean) while employing clean Python loops for custom rule evaluation, formatting, and reporting.
3. **Handling Tied Rankings**:
   - *Challenge*: Multiple students shared identical average marks (e.g., Varun and Rahul at 94.50%).
   - *Learning*: Implemented multi-column deterministic sorting (`by=['average_marks', 'attendance']`) to break ties transparently based on class participation.

---

## 10. GitHub Repository
- **Repository URL**: `https://github.com/HimanshuRana9/Student-Performance-Analytics`
- **Remote Origin**: `https://github.com/HimanshuRana9/Student-Performance-Analytics.git`
- **Default Branch**: `main`
- **Author**: Himanshu Rana (`HimanshuRana9`)
