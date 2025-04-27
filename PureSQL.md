CREATE TABLE Departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL,
        building TEXT
    )

CREATE TABLE Students (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE,
        department_id INTEGER,
        enrollment_date TEXT,
        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
    )

CREATE TABLE Courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        department_id INTEGER,
        credits INTEGER,
        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
    )

CREATE TABLE Grades (
        grade_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        grade TEXT,
        semester TEXT,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
    )

INSERT INTO Departments VALUES (1, 'Computer Science', 'Engineering Building'),
        (2, 'Mathematics', 'Science Building'),
        (3, 'Physics', 'Science Building')

INSERT INTO Students VALUES (1, 'John', 'Doe', 'john.doe@university.edu', 1, '2028-09-01'),
        (2, 'Jane', 'Smith', 'jane.smith@university.edu', 2, '2028-09-01'),
        (3, 'Bob', 'Johnson', 'bob.johnson@university.edu', 1, '2028-09-01')

INSERT INTO Courses VALUES (1, 'Introduction to Programming', 1, 3),
        (2, 'Database Systems', 1, 3),
        (3, 'Calculus I', 2, 4),
        (4, 'Physics I', 3, 4)

INSERT INTO Grades VALUES (1, 1, 1, 'A', 'Fall 2028'),
        (2, 1, 2, 'B+', 'Fall 2028'),
        (3, 2, 3, 'A-', 'Fall 2028'),
        (4, 3, 1, 'B', 'Fall 2028')

