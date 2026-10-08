"""
main.py
=======
Student Performance Analytics System - Main Application Entry Point

This program executes an end-to-end academic analytics pipeline:
1. Loads student data from 'students.csv'
2. Validates structure, data integrity, and ranges
3. Processes grades, results, and statistical metrics using NumPy and Pandas
4. Displays formatted, student-level and class-wide reports
5. Summarizes actionable insights derived strictly from verified data
"""

import sys
import functions as fn


def print_banner(title, char="=", width=88):
    """Print a visually centered banner."""
    print()
    print(char * width)
    print(title.center(width))
    print(char * width)


def print_section_header(title, char="-", width=88):
    """Print a section header with divider."""
    print()
    print(title)
    print(char * width)


def main():
    """Main execution orchestrator."""
    print_banner("STUDENT PERFORMANCE ANALYTICS SYSTEM")

    # 1. Load Data
    csv_file = "students.csv"
    raw_df = fn.load_student_data(csv_file)
    if raw_df is None:
        print("[Abort] System terminated because student data could not be loaded.")
        sys.exit(1)

    # 2. Validate Data
    is_valid, validation_msg = fn.validate_student_data(raw_df)
    if not is_valid:
        print(f"[Validation Failed] {validation_msg}")
        print("[Abort] System terminated due to invalid data.")
        sys.exit(1)

    # 3. Calculate Analytical Metrics
    df = fn.calculate_student_metrics(raw_df)

    # 4. DATASET OVERVIEW
    print_section_header("DATASET OVERVIEW")
    print(f"Total Student Records : {len(df)}")
    print(f"Total Attributes      : {df.shape[1]}")
    print(f"Attributes Included   : {', '.join(df.columns)}")
    print(f"Validation Status     : Passed (No missing/corrupt values)")

    # 5. STUDENT PERFORMANCE SUMMARY TABLE
    print_section_header("STUDENT PERFORMANCE SUMMARY")
    fn.display_student_table(df)

    # 6. CLASS PERFORMANCE
    class_stats = fn.get_class_statistics(df)
    print_section_header("CLASS PERFORMANCE")
    print(f"Total Students Enrolled : {class_stats['total_students']}")
    print(f"Overall Class Average   : {class_stats['class_average']:.2f}%")
    print(f"Highest Average Score   : {class_stats['highest_average']:.2f}% ({class_stats['top_student']['name']}, {class_stats['top_student']['department']})")
    print(f"Lowest Average Score    : {class_stats['lowest_average']:.2f}% ({class_stats['bottom_student']['name']}, {class_stats['bottom_student']['department']})")
    print(f"Students Passed         : {class_stats['passed_students']}")
    print(f"Students Failed         : {class_stats['failed_students']}")
    print(f"Overall Pass Percentage : {class_stats['pass_percentage']:.2f}%")

    # 7. SUBJECT-WISE PERFORMANCE
    subj_stats = fn.get_subject_statistics(df)
    print_section_header("SUBJECT-WISE PERFORMANCE")
    for subj_key, subj_data in subj_stats.items():
        if subj_key.startswith("_"):
            continue
        print(f"[{subj_key}]")
        print(f"  Average Score   : {subj_data['average']:.2f}")
        print(f"  Highest Score   : {subj_data['highest']}")
        print(f"  Lowest Score    : {subj_data['lowest']}")
        print(f"  Median Score    : {subj_data['median']:.2f}")
        print(f"  Std Deviation   : {subj_data['std_dev']:.2f}")

    print()
    print(f"Best Performing Subject  : {subj_stats['_summary']['best_subject']} (Average: {subj_stats['_summary']['best_subject_avg']:.2f})")
    print(f"Weakest Performing Subject: {subj_stats['_summary']['worst_subject']} (Average: {subj_stats['_summary']['worst_subject_avg']:.2f})")

    # 8. TOP PERFORMERS
    top_5_df = fn.get_top_performers(df, top_n=5)
    print_section_header("TOP PERFORMERS (TOP 5 STUDENTS)")
    top_fmt = "{:<6} {:<12} {:<14} {:<12} {:>10} {:^9} {:^8}"
    print(top_fmt.format("Rank", "Student ID", "Name", "Department", "Average", "Grade", "Result"))
    print("-" * 75)
    # Demonstrate loop with enumerate
    for rank, (_, student) in enumerate(top_5_df.iterrows(), start=1):
        print(top_fmt.format(
            f"#{rank}",
            student["student_id"],
            student["name"],
            student["department"],
            f"{student['average_marks']:.2f}%",
            student["grade"],
            student["result"]
        ))
    print("-" * 75)

    # 9. ATTENDANCE ANALYSIS
    att_stats = fn.get_attendance_analysis(df)
    print_section_header("ATTENDANCE ANALYSIS")
    print(f"Average Attendance      : {att_stats['average_attendance']:.2f}%")
    print(f"Highest Attendance      : {att_stats['highest_attendance']:.2f}%")
    print(f"Lowest Attendance       : {att_stats['lowest_attendance']:.2f}%")
    print(f"Low Attendance (< 75%)  : {att_stats['low_attendance_count']} student(s)")
    if att_stats['low_attendance_students']:
        print("  Students with < 75% attendance:")
        for s in att_stats['low_attendance_students']:
            print(f"    - {s['name']} (ID: {s['student_id']}, {s['department']}): {s['attendance']}% (Avg: {s['average_marks']:.2f}%)")
    print(f"Attendance-Marks Correlation : {att_stats['correlation_attendance_marks']:.3f} (Positive Association)")

    # 10. DEPARTMENT-WISE PERFORMANCE
    dept_df = fn.get_department_statistics(df)
    print_section_header("DEPARTMENT-WISE PERFORMANCE")
    dept_fmt = "{:<12} {:>10} {:>13} {:>13} {:>14} {:>16}"
    print(dept_fmt.format("Department", "Students", "Avg Python", "Avg ML", "Avg Overall", "Avg Attendance"))
    print("-" * 84)
    for _, dept_row in dept_df.iterrows():
        print(dept_fmt.format(
            dept_row["department"],
            dept_row["student_count"],
            f"{dept_row['avg_python']:.2f}",
            f"{dept_row['avg_ml']:.2f}",
            f"{dept_row['avg_overall']:.2f}%",
            f"{dept_row['avg_attendance']:.2f}%"
        ))
    print("-" * 84)

    # 11. FINAL INSIGHTS
    insights = fn.generate_insights(class_stats, subj_stats, dept_df, att_stats)
    print_section_header("FINAL INSIGHTS")
    for idx, insight in enumerate(insights, start=1):
        print(f"{idx}. {insight}")

    # Footer
    print_banner("Analysis completed successfully.", char="=")


if __name__ == "__main__":
    main()
