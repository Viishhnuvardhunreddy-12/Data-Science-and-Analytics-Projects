import sqlite3

## connect to Sqlite database
conn = sqlite3.connect('student.db')

## create a cursor object for executing SQL commands like select, insert, update, delete
curser = conn.cursor()

## creating table
table_info = """
create table STUDENT(NAME varchar(20), AGE int, Marks int, CITY varchar(20),SECTION varchar(20));

"""
curser.execute(table_info)

curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Arjun', 20, 85, 'Hyderabad', 'A')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Meera', 21, 90, 'Chennai', 'A')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Rahul', 19, 78, 'Delhi', 'A')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Priya', 22, 88, 'Mumbai', 'B')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Kiran', 20, 92, 'Kolkata', 'C')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Anita', 23, 76, 'Bengaluru', 'D')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Vikram', 21, 89, 'Pune', 'E')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Sita', 20, 84, 'Jaipur', 'F')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Ravi', 22, 91, 'Lucknow', 'G')''')
curser.execute('''INSERT INTO STUDENT (NAME, AGE, Marks, CITY, SECTION) VALUES ('Nisha', 19, 87, 'Ahmedabad', 'H')''')  


## Display all the Records
data = curser.execute('''select * from STUDENT''')

for row in data:
    print(row)

## commit the changes
conn.commit()

## close the connection
conn.close()

