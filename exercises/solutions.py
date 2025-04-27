import sqlite3
import os

def create_connection():
    """Create a database connection."""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory to find the database
    parent_dir = os.path.dirname(current_dir)
    # Create the full path to the database
    db_path = os.path.join(parent_dir, 'university.db')
    conn = sqlite3.connect(db_path)
    return conn

def execute_query(conn, query, params=None):
    """Execute a query and return the results."""
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()

def print_results(results, title):
    """Print query results in a formatted way."""
    print(f"\n=== {title} ===")
    for row in results:
        print(row)

def exercise_1_solutions(conn):
    """Solutions for Exercise 1: Basic SELECT"""
    # 1. Select all students who enrolled in 2023
    query = """
    SELECT * FROM Students 
    WHERE enrollment_date LIKE '2023%'
    """
    results = execute_query(conn, query)
    print_results(results, "Students enrolled in 2023")

    # 2. Select all courses with more than 3 credits
    query = """
    SELECT * FROM Courses 
    WHERE credits > 3
    """
    results = execute_query(conn, query)
    print_results(results, "Courses with more than 3 credits")

    # 3. Select all students in the Computer Science department
    query = """
    SELECT s.* FROM Students s
    JOIN Departments d ON s.department_id = d.department_id
    WHERE d.department_name = 'Computer Science'
    """
    results = execute_query(conn, query)
    print_results(results, "Computer Science Students")

def exercise_2_solutions(conn):
    """Solutions for Exercise 2: JOIN Operations"""
    # 1. Find all students and their grades
    query = """
    SELECT s.first_name, s.last_name, c.course_name, g.grade
    FROM Students s
    JOIN Grades g ON s.student_id = g.student_id
    JOIN Courses c ON g.course_id = c.course_id
    """
    results = execute_query(conn, query)
    print_results(results, "Students and their Grades")

    # 2. Find all courses offered by each department
    query = """
    SELECT d.department_name, c.course_name
    FROM Departments d
    JOIN Courses c ON d.department_id = c.department_id
    ORDER BY d.department_name
    """
    results = execute_query(conn, query)
    print_results(results, "Courses by Department")

    # 3. Find the average grade for each student
    query = """
    SELECT s.first_name, s.last_name, 
           AVG(CASE 
               WHEN g.grade = 'A' THEN 4.0
               WHEN g.grade = 'A-' THEN 3.7
               WHEN g.grade = 'B+' THEN 3.3
               WHEN g.grade = 'B' THEN 3.0
               WHEN g.grade = 'B-' THEN 2.7
               ELSE 0
           END) as average_grade
    FROM Students s
    JOIN Grades g ON s.student_id = g.student_id
    GROUP BY s.student_id, s.first_name, s.last_name
    """
    results = execute_query(conn, query)
    print_results(results, "Average Grades per Student")

def exercise_3_solutions(conn):
    """Solutions for Exercise 3: GROUP BY and Aggregations"""
    # 1. Count the number of students in each department
    query = """
    SELECT d.department_name, COUNT(s.student_id) as student_count
    FROM Departments d
    LEFT JOIN Students s ON d.department_id = s.department_id
    GROUP BY d.department_name
    """
    results = execute_query(conn, query)
    print_results(results, "Student Count per Department")

    # 2. Find the department with the most students
    query = """
    SELECT d.department_name, COUNT(s.student_id) as student_count
    FROM Departments d
    LEFT JOIN Students s ON d.department_id = s.department_id
    GROUP BY d.department_name
    ORDER BY student_count DESC
    LIMIT 1
    """
    results = execute_query(conn, query)
    print_results(results, "Department with Most Students")

    # 3. Calculate the average credits per department
    query = """
    SELECT d.department_name, AVG(c.credits) as avg_credits
    FROM Departments d
    JOIN Courses c ON d.department_id = c.department_id
    GROUP BY d.department_name
    """
    results = execute_query(conn, query)
    print_results(results, "Average Credits per Department")

def exercise_4_solutions(conn):
    """Solutions for Exercise 4: Data Modification"""
    try:
        # 1. Add a new student
        query = """
        INSERT INTO Students (student_id, first_name, last_name, email, department_id, enrollment_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (4, 'Alice', 'Williams', 'alice.williams@university.edu', 2, '2023-09-01')
        execute_query(conn, query, params)
        conn.commit()
        print("\n=== New Student Added Successfully ===")

        # 2. Update a student's email
        query = """
        UPDATE Students
        SET email = ?
        WHERE student_id = ?
        """
        params = ('new.email@university.edu', 1)
        execute_query(conn, query, params)
        conn.commit()
        print("=== Student Email Updated Successfully ===")

        # 3. Delete a course
        query = """
        DELETE FROM Courses
        WHERE course_id = ?
        """
        params = (4,)
        execute_query(conn, query, params)
        conn.commit()
        print("=== Course Deleted Successfully ===")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def exercise_5_solutions(conn):
    """Solutions for Exercise 5: Advanced Queries"""
    # 1. Find students who have taken courses from multiple departments
    query = """
    SELECT s.first_name, s.last_name, COUNT(DISTINCT c.department_id) as dept_count
    FROM Students s
    JOIN Grades g ON s.student_id = g.student_id
    JOIN Courses c ON g.course_id = c.course_id
    GROUP BY s.student_id, s.first_name, s.last_name
    HAVING COUNT(DISTINCT c.department_id) > 1
    """
    results = execute_query(conn, query)
    print_results(results, "Students with Courses from Multiple Departments")

    # 2. Find the highest grade in each course
    query = """
    SELECT c.course_name, MAX(g.grade) as highest_grade
    FROM Courses c
    JOIN Grades g ON c.course_id = g.course_id
    GROUP BY c.course_id, c.course_name
    """
    results = execute_query(conn, query)
    print_results(results, "Highest Grade per Course")

    # 3. List all students who haven't taken any courses yet
    query = """
    SELECT s.*
    FROM Students s
    LEFT JOIN Grades g ON s.student_id = g.student_id
    WHERE g.grade_id IS NULL
    """
    results = execute_query(conn, query)
    print_results(results, "Students without Courses")

def main():
    # Get the database path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    db_path = os.path.join(parent_dir, 'university.db')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found. Please run sql_basics.py first.")
        return

    # Create database connection
    conn = create_connection()
    
    try:
        print("Running Exercise 1 Solutions...")
        exercise_1_solutions(conn)
        
        print("\nRunning Exercise 2 Solutions...")
        exercise_2_solutions(conn)
        
        print("\nRunning Exercise 3 Solutions...")
        exercise_3_solutions(conn)
        
        print("\nRunning Exercise 4 Solutions...")
        exercise_4_solutions(conn)
        
        print("\nRunning Exercise 5 Solutions...")
        exercise_5_solutions(conn)
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main() 