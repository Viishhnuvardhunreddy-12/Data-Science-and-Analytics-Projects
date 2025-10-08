import streamlit as st
import pandas as pd
from reatil_sales_db import create_db, create_chain, execute_query, get_db_uri

st.set_page_config(page_title="Retail Sales SQL Explorer", layout="wide")

st.title("Retail Sales SQL Explorer")
st.write("Use natural language to query the retail sales MySQL database. The app will generate SQL using Gemini and show results.")

# Sidebar for configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="GEMINI_API_KEY or enter here")
st.sidebar.markdown("---")
st.sidebar.subheader("Database connection (optional)")
col1, col2 = st.sidebar.columns(2)
with col1:
    db_user = st.text_input("DB user", value="root")
with col2:
    db_password = st.text_input("DB password", value="root", type="password")
col3, col4 = st.sidebar.columns(2)
with col3:
    db_host = st.text_input("DB host", value="localhost")
with col4:
    db_name = st.text_input("DB name", value="retail_sales_db")

if st.sidebar.button("Test connection and load schema"):
    uri = get_db_uri(db_user, db_password, db_host, db_name)
    try:
        db = create_db(uri)
        st.sidebar.success("Connected to database")
        # small schema preview
        try:
            tables = db.get_table_names()
            st.sidebar.write("Tables:")
            st.sidebar.write(tables)
        except Exception:
            st.sidebar.info("Could not list tables (insufficient privileges?)")
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")


# Main interaction area
st.header("Ask a question (natural language)")
question = st.text_input("Enter question", value="List the top 5 products by sales amount.")
col_a, col_b = st.columns([3,1])
with col_b:
    if st.button("Run"):
        st.session_state.run = True

# Keep a history of questions/results in session state
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Clear history"):
    st.session_state.history = []

if st.session_state.get("run"):
    st.session_state.run = False
    # create DB and chain
    uri = get_db_uri(db_user, db_password, db_host, db_name)
    try:
        db = create_db(uri)
    except Exception as e:
        st.error(f"Could not connect to DB: {e}")
        st.stop()

    try:
        chain = create_chain(api_key, db)
    except Exception as e:
        st.error(f"Could not create LLM chain: {e}")
        st.stop()

    with st.spinner("Generating SQL and running query..."):
        out = execute_query(chain, question, db)

    if out["error"]:
        st.error(out["error"])
    else:
        sql = out["sql"]
        rows = out["rows"]
        st.subheader("Generated SQL")
        st.code(sql or "(no SQL returned)")

        st.subheader("Results")
        if rows is None:
            st.info("No rows returned or an error occurred when running SQL.")
        else:
            # rows may be list of dicts, or list of tuples depending on SQLDatabase
            try:
                if isinstance(rows, list):
                    if len(rows) == 0:
                        st.write("Query returned 0 rows")
                    else:
                        # convert to DataFrame intelligently
                        if isinstance(rows[0], dict):
                            df = pd.DataFrame(rows)
                        else:
                            df = pd.DataFrame(rows)
                        st.dataframe(df)
                else:
                    st.write(rows)
            except Exception as e:
                st.write(rows)
                st.warning(f"Could not render results as table: {e}")

        # append to history
        st.session_state.history.append({"question": question, "sql": sql, "rows": rows})

# Show history
if st.session_state.history:
    st.markdown("---")
    st.subheader("History")
    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Q: {item['question']}", expanded=False):
            st.code(item.get("sql") or "(no SQL)")
            if item.get("rows"):
                try:
                    df = pd.DataFrame(item["rows"])
                    st.dataframe(df)
                except Exception:
                    st.write(item["rows"])

st.markdown("---")
st.caption("This demo converts natural language to SQL using Google Gemini via langchain and runs it against a MySQL database. Use with caution and avoid running destructive statements.")
