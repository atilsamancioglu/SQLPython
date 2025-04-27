import sqlite3
import os

def create_database():
    """Create a new SQLite database and establish connection."""
    # Remove existing database if it exists
    if os.path.exists('university.db'):
        os.remove('university.db')
    
    # Create a new database
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):
    """Create necessary tables for the university database."""
    # Create Departments table first (no foreign keys)
    cursor.execute('''
    CREATE TABLE Departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL,
        building TEXT
    )
    ''')

    # Create Students table (references Departments)
    cursor.execute('''
    CREATE TABLE Students (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE,
        department_id INTEGER,
        enrollment_date TEXT,
        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
    )
    ''')

    # Create Courses table (references Departments)
    cursor.execute('''
    CREATE TABLE Courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        department_id INTEGER,
        credits INTEGER,
        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
    )
    ''')

    # Create Grades table last (references both Students and Courses)
    cursor.execute('''
    CREATE TABLE Grades (
        grade_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        grade TEXT,
        semester TEXT,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
    )
    ''')

def insert_sample_data(cursor):
    """Insert sample data into the tables."""
    # Insert departments
    departments = [
        (1, 'Computer Science', 'Engineering Building'),
        (2, 'Mathematics', 'Science Building'),
        (3, 'Physics', 'Science Building')
    ]
    cursor.executemany('INSERT INTO Departments VALUES (?, ?, ?)', departments)

    # Insert students
    students = [
        (1, 'John', 'Doe', 'john.doe@university.edu', 1, '2028-09-01'),
        (2, 'Jane', 'Smith', 'jane.smith@university.edu', 2, '2028-09-01'),
        (3, 'Bob', 'Johnson', 'bob.johnson@university.edu', 1, '2028-09-01')
    ]
    cursor.executemany('INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?)', students)

    # Insert courses
    courses = [
        (1, 'Introduction to Programming', 1, 3),
        (2, 'Database Systems', 1, 3),
        (3, 'Calculus I', 2, 4),
        (4, 'Physics I', 3, 4)
    ]
    cursor.executemany('INSERT INTO Courses VALUES (?, ?, ?, ?)', courses)

    # Insert grades
    grades = [
        (1, 1, 1, 'A', 'Fall 2028'),
        (2, 1, 2, 'B+', 'Fall 2028'),
        (3, 2, 3, 'A-', 'Fall 2028'),
        (4, 3, 1, 'B', 'Fall 2028')
    ]
    cursor.executemany('INSERT INTO Grades VALUES (?, ?, ?, ?, ?)', grades)

def demonstrate_queries(cursor):
    """Demonstrate various SQL queries."""
    print("\n=== SELECT ALL STUDENTS ===")
    cursor.execute("SELECT * FROM Students")
    print("All Students:")
    for row in cursor.fetchall():
        print(row)

    print("\n=== SELECT ALL DEPARTMENTS ===")
    cursor.execute("SELECT * FROM Departments")
    print("All Departments:")
    for row in cursor.fetchall():
        print(row)

    print("\n=== WHERE Clause ===")
    cursor.execute("SELECT * FROM Students WHERE department_id = 1")
    print("Computer Science Students:")
    for row in cursor.fetchall():
        print(row)

    print("\n=== JOIN Operation ===")
    cursor.execute('''
    SELECT s.first_name, s.last_name, d.department_name
    FROM Students s
    JOIN Departments d ON s.department_id = d.department_id
    ''')
    print("Students with their Departments:")
    for row in cursor.fetchall():
        print(row)

    print("\n=== GROUP BY and Aggregate Functions ===")
    cursor.execute('''
    SELECT d.department_name, COUNT(s.student_id) as student_count
    FROM Departments d
    LEFT JOIN Students s ON d.department_id = s.department_id
    GROUP BY d.department_name
    ''')
    print("Number of Students per Department:")
    for row in cursor.fetchall():
        print(row)

def main():
    # Create database and get connection
    conn, cursor = create_database()
    
    try:
        # Create tables
        create_tables(cursor)
        
        # Insert sample data
        insert_sample_data(cursor)
        
        # Demonstrate queries
        demonstrate_queries(cursor)
        
        # Commit changes
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close connection
        conn.close()

if __name__ == "__main__":
    main() 