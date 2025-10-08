import os
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from dotenv import load_dotenv

load_dotenv()

# Default DB connection parameters (editable by the Streamlit app)
DB_DEFAULTS = {
    "db_user": os.getenv("DB_USER", "root"),
    "db_password": os.getenv("DB_PASSWORD", "root"),
    "db_host": os.getenv("DB_HOST", "localhost"),
    "db_name": os.getenv("DB_NAME", "retail_sales_db"),
}


def get_db_uri(db_user=None, db_password=None, db_host=None, db_name=None):
    """Return a SQLAlchemy URI for the MySQL database.

    This is a thin helper so the Streamlit app can override connection values safely.
    """
    db_user = db_user or DB_DEFAULTS["db_user"]
    db_password = db_password or DB_DEFAULTS["db_password"]
    db_host = db_host or DB_DEFAULTS["db_host"]
    db_name = db_name or DB_DEFAULTS["db_name"]
    return f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'


def create_db(db_uri: str = None):
    """Create and return a SQLDatabase instance from the given URI.

    Note: we keep DB creation lazy so importing this module doesn't attempt network/database work.
    """
    uri = db_uri or get_db_uri()
    return SQLDatabase.from_uri(uri)


def create_chain(api_key: str | None, db: SQLDatabase):
    """Create and return a SQL query chain that converts natural language to SQL.

    api_key may be provided (e.g., from the Streamlit UI). If not provided, the environment
    variable GEMINI_API_KEY is used.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("No GEMINI API key provided. Set GEMINI_API_KEY or provide it in the app.")

    # Lazy import to avoid import-time errors when the google generative package is not available
    try:
        from langchain_google_genai import GoogleGenerativeAI
    except Exception as e:
        raise ImportError(f"Could not import GoogleGenerativeAI: {e}. Ensure required packages are installed.")

    llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=key)
    # create_sql_query_chain returns a chain that, when invoked with a question, returns the SQL
    chain = create_sql_query_chain(llm, db)
    return chain


def execute_query(chain, question: str, db: SQLDatabase):
    """Given a chain and NL question, return a dict with the generated SQL and query results.

    Returns: {"sql": str, "rows": list, "error": str|None}
    """
    try:
        response = chain.invoke({"question": question})

        # The chain may return a plain string SQL or a dict-like object; coerce to string when possible
        sql = None
        if isinstance(response, str):
            sql = response
        else:
            # Try common keys
            sql = getattr(response, "sql", None) or (response.get("sql") if isinstance(response, dict) else None) or str(response)

        # Clean the SQL: remove leading descriptors, code fences, and stray words like 'sql' or 'SQLQuery:'
        if isinstance(sql, str):
            # Remove common prefixes
            prefixes = ["SQLQuery:", "SQL:", "sql:", "sql", "SQLQuery"]
            s = sql.strip()
            # If starts with a prefix, remove it
            for p in prefixes:
                if s.startswith(p):
                    s = s[len(p):].lstrip(':').strip()

            # Remove triple/back tick code fences
            if s.startswith("```") and s.endswith("```"):
                s = s.strip("`\n ")

            # If model outputs something like 'sql\nSELECT ...', drop any leading non-SQL lines
            lines = [ln for ln in s.splitlines()]
            # find first line that looks like SQL (starts with SELECT, WITH, INSERT, UPDATE, DELETE, etc.)
            sql_start_idx = None
            sql_keywords = ("select", "with", "insert", "update", "delete", "create", "drop", "alter")
            for idx, ln in enumerate(lines):
                if ln.strip() == "":
                    continue
                low = ln.strip().lower()
                # also allow lines that start with SQL comment or parentheses
                if any(low.startswith(k) for k in sql_keywords) or low.startswith("("):
                    sql_start_idx = idx
                    break

            if sql_start_idx is not None:
                cleaned = "\n".join(lines[sql_start_idx:]).strip()
            else:
                # fallback: use the full stripped text
                cleaned = s.strip()

            sql = cleaned

        # Run the SQL against the DB and return rows
        rows = []
        if sql:
            try:
                rows = db.run(sql)
            except Exception as e:
                return {"sql": sql, "rows": None, "error": f"DB error: {e}"}

        return {"sql": sql, "rows": rows, "error": None}
    except Exception as e:
        return {"sql": None, "rows": None, "error": f"Chain error: {e}"}
