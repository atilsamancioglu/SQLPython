# SQL Exercise Solutions

## Exercise 1: Basic SELECT

1. Select all students who enrolled in 2023:
```sql
SELECT * FROM Students 
WHERE enrollment_date LIKE '2023%';
```

2. Select all courses with more than 3 credits:
```sql
SELECT * FROM Courses 
WHERE credits > 3;
```

3. Select all students in the Computer Science department:
```sql
SELECT s.* FROM Students s
JOIN Departments d ON s.department_id = d.department_id
WHERE d.department_name = 'Computer Science';
```

## Exercise 2: JOIN Operations

1. Find all students and their grades:
```sql
SELECT s.first_name, s.last_name, c.course_name, g.grade
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
JOIN Courses c ON g.course_id = c.course_id;
```

2. Find all courses offered by each department:
```sql
SELECT d.department_name, c.course_name
FROM Departments d
JOIN Courses c ON d.department_id = c.department_id
ORDER BY d.department_name;
```

3. Find the average grade for each student:
```sql
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
GROUP BY s.student_id, s.first_name, s.last_name;
```

## Exercise 3: GROUP BY and Aggregations

1. Count the number of students in each department:
```sql
SELECT d.department_name, COUNT(s.student_id) as student_count
FROM Departments d
LEFT JOIN Students s ON d.department_id = s.department_id
GROUP BY d.department_name;
```

2. Find the department with the most students:
```sql
SELECT d.department_name, COUNT(s.student_id) as student_count
FROM Departments d
LEFT JOIN Students s ON d.department_id = s.department_id
GROUP BY d.department_name
ORDER BY student_count DESC
LIMIT 1;
```

3. Calculate the average credits per department:
```sql
SELECT d.department_name, AVG(c.credits) as avg_credits
FROM Departments d
JOIN Courses c ON d.department_id = c.department_id
GROUP BY d.department_name;
```

## Exercise 4: Data Modification

1. Add a new student to the database:
```sql
INSERT INTO Students (student_id, first_name, last_name, email, department_id, enrollment_date)
VALUES (4, 'Alice', 'Williams', 'alice.williams@university.edu', 2, '2023-09-01');
```

2. Update a student's email address:
```sql
UPDATE Students
SET email = 'new.email@university.edu'
WHERE student_id = 1;
```

3. Delete a course from the database:
```sql
DELETE FROM Courses
WHERE course_id = 4;
```

## Exercise 5: Advanced Queries

1. Find students who have taken courses from multiple departments:
```sql
SELECT s.first_name, s.last_name, COUNT(DISTINCT c.department_id) as dept_count
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
JOIN Courses c ON g.course_id = c.course_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(DISTINCT c.department_id) > 1;
```

2. Find the highest grade in each course:
```sql
SELECT c.course_name, MAX(g.grade) as highest_grade
FROM Courses c
JOIN Grades g ON c.course_id = g.course_id
GROUP BY c.course_id, c.course_name;
```

3. List all students who haven't taken any courses yet:
```sql
SELECT s.*
FROM Students s
LEFT JOIN Grades g ON s.student_id = g.student_id
WHERE g.grade_id IS NULL;
```

## Notes
- These solutions assume the database structure and sample data from the main script
- Some queries might need adjustment based on the actual data in your database
- The grade conversion in the average grade calculation is simplified for demonstration
- Always test these queries in a development environment before running them on production data 