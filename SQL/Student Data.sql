-- Retrieve all student records from the Students table.
select * from students;

-- Display only the first name, last name, and email of all students.
select first_name,last_name, email
from students;

-- List all courses that have 4 credits.
select course_name
from courses where credits = 4;

-- Show the faculty names who are from the "Computer Science" department.
select concat(first_name,' ' ,last_name) as fullname from faculty where department = 'Computer Science';

-- Find all students born after 2002-01-01.
select * from students where dob > '2002-01-01';

-- Retrieve students whose first name starts with ‘A’.
select * from students where first_name like 'A%';
select * from students where first_name regexp '^A';

-- List all courses ordered by credits in descending order.
select * from courses order by credits desc;

-- Find students whose email ends with @example.com.
select * from students where email regexp '@example.com$';

-- Count the total number of students.
select distinct count(*) as total_count from students;

-- Find the average credits of all courses.
select avg(credits) as avg_credits from courses;

-- Show the number of courses offered by each department.
select count(c.course_id) as no_of_courses,department
from courses as c
join faculty as f
on c.faculty_id = f.faculty_id -- using faculty_id it is better when the columns are having similar names
group by department
order by no_of_courses desc;

-- Display each student’s first name along with the course names they are enrolled in.
select s.first_name, s.last_name,semester,course_name
from students s
join enrollments e
on s.student_id = e.student_id
join courses c
on c.course_id = e.course_id
order by s.first_name;

-- Show the courses along with the faculty who teach them.
select concat(f.first_name,' ',f.last_name) as faculty, c.course_name
from courses c
join faculty f
on c.faculty_id = f.faculty_id
order by f.first_name;

-- Retrieve the list of students with their course name, semester, and grade.
select concat(s.first_name,' ',last_name) as student, c.course_name, e.semester, e.grade
from students s
join enrollments e
on s.student_id = e.student_id
join courses c
on c.course_id = e.course_id
order by student;

-- Find all students enrolled in courses taught by Kavita Rao.
select concat(s.first_name,' ',s.last_name) as student, c.course_name,concat(f.first_name,' ',f.last_name) as faculty
from students s
join enrollments e
on s.student_id = e.student_id
join courses c
on e.course_id = c.course_id
join faculty f
on f.faculty_id = c.faculty_id
where concat(f.first_name,' ',f.last_name) = 'Kavita Rao';

-- Find the names of students who are enrolled in more than 2 courses.
select s.student_id,concat(s.first_name,' ',s.last_name) as student, count(e.course_id) as course_count
from students s
join enrollments e
on s.student_id = e.student_id
group by s.student_id
having course_count >= 2;

-- List the students who got an ‘A’ grade in at least one course.
select s.student_id,concat(s.first_name,' ',s.last_name) as student, e.grade
from students s
join enrollments e
on s.student_id = e.student_id
where e.grade = 'A'
order by student;

