# Prompt2SQL Project README

Prompt2SQL is a web application that converts natural language questions into SQL queries using Google Gemini AI. Users can type a question about their database, and the app generates and executes the SQL query, displaying results interactively using Streamlit and Pandas.

---

## Features

- Convert natural language questions to SQL automatically using Google Gemini-2.5-flash.
- Supports joins, aggregation, filtering, ordering, subqueries, and limits.
- Execute SQL queries on a SQLite database and view results in a clean table format.
- Built with Streamlit, SQLite, Pandas, and Google Generative AI.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv texttosqlvenv
```

### 3. Activate the Virtual Environment

- **Windows:**

```bash
texttosqlvenv\Scripts\activate
```

- **Linux / macOS:**

```bash
source texttosqlvenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure your `requirements.txt` includes:
> ```
> streamlit
> google-generativeai
> python-dotenv
> pandas
> sqlite3
> ```

### 5. Set Your Gemini API Key

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the Streamlit App

```bash
streamlit run app.py
```

The app should open in your default browser at `http://localhost:8501`.

---

## Usage

1. Enter your natural language question about the database in the input box.
2. Click **Generate SQL Query**.
3. View the **generated SQL query** and the **query results** displayed in an interactive table.

---

## Database

- The app uses a sample SQLite database called `student.db`.
- Ensure the database file is in the project root.
- Sample tables include:
  - `STUDENT(NAME, AGE, MARKS, CITY, SECTION)`
  - `TEACHER(ID, NAME, SECTION)`

---

## License

This project is licensed under the MIT License.

---

## Screenshots

*(Optional: Add screenshots of your app UI here)*

---

Made with ❤️ using Python, Streamlit, Pandas, and Google Gemini AI