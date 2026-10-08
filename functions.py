"""
functions.py
============
Student Performance Analytics System - Core Reusable Functions Module

This module contains modular, beginner-friendly, and reusable functions for:
- Loading and validating student CSV datasets
- Calculating total marks, average marks, grades, and pass/fail results
- Computing subject-wise and class-wide descriptive statistics using NumPy & Pandas
- Performing attendance and department-level aggregations
- Generating structured console tables and analytical insights
"""

import pandas as pd
import numpy as np


def load_student_data(filepath="students.csv"):
    """
    Load student dataset from a CSV file into a pandas DataFrame with error handling.

    Parameters:
        filepath (str): The path to the CSV file. Default is 'students.csv'.

    Returns:
        pd.DataFrame or None: Loaded DataFrame if successful, None if an error occurs.
    """
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            print(f"[Error] The file '{filepath}' is empty.")
            return None
        return df
    except FileNotFoundError:
        print(f"[Error] The file '{filepath}' was not found. Please verify the file path.")
        return None
    except pd.errors.EmptyDataError:
        print(f"[Error] The file '{filepath}' contains no data.")
        return None
    except Exception as e:
        print(f"[Error] An unexpected error occurred while loading '{filepath}': {e}")
        return None


def validate_student_data(df):
    """
    Perform validation checks on the loaded student DataFrame.

    Checks:
    - Required columns exist
    - No critical missing values in essential fields
    - Correct numeric data types for marks and attendance
    - Numeric values fall within sensible ranges (0-100 for marks and attendance)
    - Identification of duplicate records

    Parameters:
        df (pd.DataFrame): The raw student DataFrame.

    Returns:
        tuple (bool, str): (True, "Valid") if validation succeeds, or (False, error_message).
    """
    if df is None or not isinstance(df, pd.DataFrame):
        return False, "Input data is not a valid pandas DataFrame."

    if df.empty:
        return False, "The dataset has zero records."

    required_columns = [
        "student_id",
        "name",
        "department",
        "year",
        "age",
        "attendance",
        "python_marks",
        "ml_marks",
        "projects_completed"
    ]

    # 1. Check for required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return False, f"Missing required column(s): {', '.join(missing_cols)}"

    # 2. Check for missing values in critical fields
    critical_cols = ["student_id", "name", "department", "attendance", "python_marks", "ml_marks"]
    missing_counts = df[critical_cols].isnull().sum()
    cols_with_nulls = missing_counts[missing_counts > 0]
    if not cols_with_nulls.empty:
        null_details = ", ".join([f"{col}: {cnt}" for col, cnt in cols_with_nulls.items()])
        return False, f"Missing values detected in critical columns: {null_details}"

    # 3. Check data types and numeric convertibility
    numeric_cols = ["attendance", "python_marks", "ml_marks"]
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False, f"Column '{col}' must contain numeric data."

    # 4. Range validation using NumPy logic
    marks_attendance = df[["python_marks", "ml_marks", "attendance"]].to_numpy()
    if np.any(marks_attendance < 0) or np.any(marks_attendance > 100):
        return False, "Marks and attendance values must be between 0 and 100."

    # 5. Check for duplicate student IDs
    duplicates = df["student_id"].duplicated().sum()
    if duplicates > 0:
        print(f"[Warning] Found {duplicates} duplicate student_id record(s).")

    return True, "Data validation passed successfully."


def assign_grade(average_marks):
    """
    Assign an academic letter grade based on a student's average marks.

    Grading Policy:
    - >= 90.0: A+
    - >= 80.0: A
    - >= 70.0: B
    - >= 60.0: C
    - >= 50.0: D
    - >= 40.0: E
    - Below 40.0: F

    Parameters:
        average_marks (float): The student's average marks.

    Returns:
        str: Assigned letter grade.
    """
    if average_marks >= 90.0:
        return "A+"
    elif average_marks >= 80.0:
        return "A"
    elif average_marks >= 70.0:
        return "B"
    elif average_marks >= 60.0:
        return "C"
    elif average_marks >= 50.0:
        return "D"
    elif average_marks >= 40.0:
        return "E"
    else:
        return "F"


def determine_pass_fail(average_marks, python_marks, ml_marks):
    """
    Determine whether a student passes or fails according to academic rules.

    Pass Rule:
    A student passes IF AND ONLY IF:
    1. Average marks >= 40.0
    2. python_marks >= 33.0
    3. ml_marks >= 33.0
    Otherwise, the student fails.

    Parameters:
        average_marks (float): Average score across subjects.
        python_marks (float or int): Score in Python.
        ml_marks (float or int): Score in Machine Learning.

    Returns:
        str: 'Pass' or 'Fail'.
    """
    if average_marks >= 40.0 and python_marks >= 33.0 and ml_marks >= 33.0:
        return "Pass"
    else:
        return "Fail"


def calculate_student_metrics(df):
    """
    Calculate calculated fields: total_marks, average_marks, grade, and result.

    Uses NumPy arrays and Python iteration to demonstrate multiple core concepts.

    Parameters:
        df (pd.DataFrame): Validated student DataFrame.

    Returns:
        pd.DataFrame: A copy of the DataFrame with added analytical columns.
    """
    processed_df = df.copy()

    # NumPy array addition for total marks
    python_arr = processed_df["python_marks"].to_numpy(dtype=float)
    ml_arr = processed_df["ml_marks"].to_numpy(dtype=float)
    total_arr = np.add(python_arr, ml_arr)

    # Average marks calculation using NumPy division
    average_arr = np.divide(total_arr, 2.0)

    # Assign total and average marks to DataFrame
    processed_df["total_marks"] = total_arr.astype(int)
    processed_df["average_marks"] = np.round(average_arr, 2)

    # Use loops and conditions to assign grade and result for each student
    grades = []
    results = []
    for idx in range(len(processed_df)):
        avg = processed_df.loc[idx, "average_marks"]
        py_mark = processed_df.loc[idx, "python_marks"]
        ml_mark = processed_df.loc[idx, "ml_marks"]

        grade = assign_grade(avg)
        res = determine_pass_fail(avg, py_mark, ml_mark)

        grades.append(grade)
        results.append(res)

    processed_df["grade"] = grades
    processed_df["result"] = results

    return processed_df


def get_subject_statistics(df, subjects=None):
    """
    Compute subject-level descriptive statistics using NumPy.

    Parameters:
        df (pd.DataFrame): Processed student DataFrame.
        subjects (dict): Dictionary mapping column names to readable names.

    Returns:
        dict: Statistical summary for each subject plus best and worst subjects.
    """
    if subjects is None:
        subjects = {
            "python_marks": "Python",
            "ml_marks": "Machine Learning"
        }

    stats = {}
    best_subject = None
    worst_subject = None
    highest_avg = -1.0
    lowest_avg = 101.0

    # Loop over subjects to calculate metrics with NumPy
    for col, display_name in subjects.items():
        arr = df[col].to_numpy(dtype=float)
        mean_val = float(np.mean(arr))
        max_val = float(np.max(arr))
        min_val = float(np.min(arr))
        median_val = float(np.median(arr))
        std_val = float(np.std(arr))

        stats[display_name] = {
            "column": col,
            "average": round(mean_val, 2),
            "highest": int(max_val),
            "lowest": int(min_val),
            "median": round(median_val, 2),
            "std_dev": round(std_val, 2)
        }

        if mean_val > highest_avg:
            highest_avg = mean_val
            best_subject = display_name

        if mean_val < lowest_avg:
            lowest_avg = mean_val
            worst_subject = display_name

    stats["_summary"] = {
        "best_subject": best_subject,
        "best_subject_avg": round(highest_avg, 2),
        "worst_subject": worst_subject,
        "worst_subject_avg": round(lowest_avg, 2)
    }

    return stats


def get_class_statistics(df):
    """
    Compute overall class-wide performance metrics using NumPy and Pandas.

    Parameters:
        df (pd.DataFrame): Processed student DataFrame.

    Returns:
        dict: Summary of overall class statistics.
    """
    total_students = len(df)
    avg_marks_array = df["average_marks"].to_numpy(dtype=float)

    # NumPy calculations
    class_average = float(np.mean(avg_marks_array))
    highest_average = float(np.max(avg_marks_array))
    lowest_average = float(np.min(avg_marks_array))

    # Identify top and bottom scoring students
    top_student_row = df.loc[df["average_marks"].idxmax()]
    bottom_student_row = df.loc[df["average_marks"].idxmin()]

    # Pass / Fail counts using boolean filtering
    passed_students = int((df["result"] == "Pass").sum())
    failed_students = int((df["result"] == "Fail").sum())
    pass_percentage = (passed_students / total_students) * 100.0 if total_students > 0 else 0.0

    return {
        "total_students": total_students,
        "class_average": round(class_average, 2),
        "highest_average": round(highest_average, 2),
        "lowest_average": round(lowest_average, 2),
        "top_student": {
            "student_id": int(top_student_row["student_id"]),
            "name": str(top_student_row["name"]),
            "department": str(top_student_row["department"]),
            "average": round(float(top_student_row["average_marks"]), 2),
            "grade": str(top_student_row["grade"])
        },
        "bottom_student": {
            "student_id": int(bottom_student_row["student_id"]),
            "name": str(bottom_student_row["name"]),
            "department": str(bottom_student_row["department"]),
            "average": round(float(bottom_student_row["average_marks"]), 2),
            "grade": str(bottom_student_row["grade"])
        },
        "passed_students": passed_students,
        "failed_students": failed_students,
        "pass_percentage": round(pass_percentage, 2)
    }


def get_top_performers(df, top_n=5):
    """
    Retrieve the top N performing students sorted by average marks in descending order.

    Parameters:
        df (pd.DataFrame): Processed student DataFrame.
        top_n (int): Number of top performers to return.

    Returns:
        pd.DataFrame: Sorted DataFrame of top performers.
    """
    # Sort by average_marks descending; if tied, sort by attendance descending
    sorted_df = df.sort_values(
        by=["average_marks", "attendance"],
        ascending=[False, False]
    ).reset_index(drop=True)

    limit = min(top_n, len(sorted_df))
    return sorted_df.head(limit)


def get_attendance_analysis(df):
    """
    Analyze student attendance figures and attendance-to-performance patterns.

    Parameters:
        df (pd.DataFrame): Processed student DataFrame.

    Returns:
        dict: Attendance statistics and low-attendance list.
    """
    attendance_arr = df["attendance"].to_numpy(dtype=float)

    mean_att = float(np.mean(attendance_arr))
    max_att = float(np.max(attendance_arr))
    min_att = float(np.min(attendance_arr))

    # Low attendance threshold (< 75%)
    low_att_df = df[df["attendance"] < 75][["student_id", "name", "department", "attendance", "average_marks"]]

    # Correlation observation between attendance and average marks
    corr = float(df["attendance"].corr(df["average_marks"]))

    return {
        "average_attendance": round(mean_att, 2),
        "highest_attendance": round(max_att, 2),
        "lowest_attendance": round(min_att, 2),
        "low_attendance_count": len(low_att_df),
        "low_attendance_students": low_att_df.to_dict(orient="records"),
        "correlation_attendance_marks": round(corr, 3)
    }


def get_department_statistics(df):
    """
    Perform department-level aggregation using Pandas groupby().

    Parameters:
        df (pd.DataFrame): Processed student DataFrame.

    Returns:
        pd.DataFrame: Aggregated department statistics.
    """
    dept_summary = df.groupby("department").agg(
        student_count=("student_id", "count"),
        avg_python=("python_marks", "mean"),
        avg_ml=("ml_marks", "mean"),
        avg_overall=("average_marks", "mean"),
        avg_attendance=("attendance", "mean")
    ).reset_index()

    dept_summary["avg_python"] = dept_summary["avg_python"].round(2)
    dept_summary["avg_ml"] = dept_summary["avg_ml"].round(2)
    dept_summary["avg_overall"] = dept_summary["avg_overall"].round(2)
    dept_summary["avg_attendance"] = dept_summary["avg_attendance"].round(2)

    # Sort departments by overall average descending
    dept_summary = dept_summary.sort_values(by="avg_overall", ascending=False).reset_index(drop=True)
    return dept_summary


def display_student_table(df):
    """
    Format and print the student performance table cleanly to the terminal.

    Parameters:
        df (pd.DataFrame): Processed student DataFrame.
    """
    header_fmt = "{:<5} {:<10} {:<12} {:>10} {:>8} {:>6} {:>7} {:>9} {:^7} {:^8}"
    row_fmt    = "{:<5} {:<10} {:<12} {:>9}% {:>8} {:>6} {:>7} {:>9.2f} {:^7} {:^8}"
    divider = "-" * 88

    print(header_fmt.format("ID", "Name", "Department", "Attendance", "Python", "ML", "Total", "Average", "Grade", "Result"))
    print(divider)

    # Demonstrate Python iteration over rows
    for _, row in df.iterrows():
        print(row_fmt.format(
            row["student_id"],
            row["name"],
            row["department"],
            row["attendance"],
            row["python_marks"],
            row["ml_marks"],
            row["total_marks"],
            row["average_marks"],
            row["grade"],
            row["result"]
        ))
    print(divider)


def generate_insights(class_stats, subj_stats, dept_stats, att_stats):
    """
    Generate factual, calculated analytical takeaways.

    Parameters:
        class_stats (dict): Class statistics.
        subj_stats (dict): Subject statistics.
        dept_stats (pd.DataFrame): Department statistics.
        att_stats (dict): Attendance statistics.

    Returns:
        list of str: Concise analytical insight statements.
    """
    top_dept = dept_stats.iloc[0]
    insights = [
        f"Top Academic Performer: {class_stats['top_student']['name']} (ID: {class_stats['top_student']['student_id']}, {class_stats['top_student']['department']}) secured highest average of {class_stats['top_student']['average']}% (Grade {class_stats['top_student']['grade']}).",
        f"Lowest Academic Performer: {class_stats['bottom_student']['name']} (ID: {class_stats['bottom_student']['student_id']}, {class_stats['bottom_student']['department']}) obtained average of {class_stats['bottom_student']['average']}% (Grade {class_stats['bottom_student']['grade']}).",
        f"Subject Comparison: {subj_stats['_summary']['best_subject']} performed best with an average of {subj_stats['_summary']['best_subject_avg']}%, outperforming {subj_stats['_summary']['worst_subject']} ({subj_stats['_summary']['worst_subject_avg']}%).",
        f"Overall Class Performance: Class average is {class_stats['class_average']}% across {class_stats['total_students']} students with a {class_stats['pass_percentage']}% pass rate ({class_stats['passed_students']} Passed, {class_stats['failed_students']} Failed).",
        f"Department Highlights: {top_dept['department']} led with the highest departmental average of {top_dept['avg_overall']}% across {top_dept['student_count']} enrolled students.",
        f"Attendance Overview: Average student attendance stands at {att_stats['average_attendance']}%, ranging from a minimum of {att_stats['lowest_attendance']}% to a peak of {att_stats['highest_attendance']}%.",
        f"Attendance Pattern Observation: Dataset exhibits a positive correlation ({att_stats['correlation_attendance_marks']}) between attendance and average academic marks."
    ]
    return insights
