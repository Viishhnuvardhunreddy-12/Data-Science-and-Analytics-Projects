from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="💻Prompt2SQL APP", page_icon=":crystal_ball:", layout="wide")
st.title("Prompt2SQL")
st.header("Convert Natural Language to SQL Query using Gemini")

# Function to get Gemini response
def get_gemini_response(prompt, question):
    # Use a valid Gemini model
    model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-1.5-pro" if 2.5 not available
    response = model.generate_content([prompt, f"Question: {question}"])
    return response.text.strip()  # remove extra whitespace

# Function to execute SQL query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
    except Exception as e:
        rows = []
        columns = []
        st.error(f"SQL Execution Error: {e}")
    conn.commit()
    conn.close()
    return rows, columns

# SQL Prompt template
prompt = """
You are an expert in converting natural language to SQL queries. 
Given a database schema and a natural language question, generate only the corresponding SQL query as text.
Do not include any explanation or results.

### Example 1 (Simple SELECT):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION)
Question: Show all students from Delhi.
SQL: SELECT * FROM STUDENT WHERE CITY = 'Delhi';

### Example 2 (Filtering with condition):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION)
Question: Get the names of students who scored more than 80 marks.
SQL: SELECT NAME FROM STUDENT WHERE MARKS > 80;

### Example 3 (Aggregation + Group By):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION)
Question: Find the average marks of students in each section.
SQL: SELECT SECTION, AVG(MARKS) FROM STUDENT GROUP BY SECTION;

### Example 4 (Ordering):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION)
Question: List students in descending order of marks.
SQL: SELECT * FROM STUDENT ORDER BY MARKS DESC;

### Example 5 (Join):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION), TEACHER(ID, NAME, SECTION)
Question: Get student names along with their teacher names.
SQL: SELECT S.NAME AS StudentName, T.NAME AS TeacherName 
     FROM STUDENT S 
     JOIN TEACHER T ON S.SECTION = T.SECTION;

### Example 6 (Subquery):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION)
Question: Find students who scored above the average marks.
SQL: SELECT NAME FROM STUDENT 
     WHERE MARKS > (SELECT AVG(MARKS) FROM STUDENT);

### Example 7 (LIMIT + OFFSET):
Schema: STUDENT(NAME, AGE, MARKS, CITY, SECTION)
Question: Show the top 5 highest scoring students.
SQL: SELECT NAME, MARKS FROM STUDENT ORDER BY MARKS DESC LIMIT 5;
"""

# Streamlit user input
st.write("Enter your question about the student database:")
user_input = st.text_input("Your Question:", key="input")
submit = st.button("Generate SQL Query")

# Handle button click
if submit:
    if user_input.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        # Get SQL query from Gemini
        sql_query = get_gemini_response(prompt, user_input)
        st.subheader("Generated SQL Query:")
        st.code(sql_query)

        # Execute SQL and display results
        data, columns = read_sql_query(sql_query, "student.db")
        if data:
            df = pd.DataFrame(data, columns=columns)
            st.subheader("Query Results:")
            st.dataframe(df)
        else:
            st.info("No results to display or SQL execution failed.")
