# 🧠 Retail Sales SQL Explorer

Ever wanted to talk to your **MySQL database in plain English**?  
This app makes that possible — powered by **Streamlit**, **LangChain**, and **Google Gemini API**.

---

## 🚀 Overview

**Retail Sales SQL Explorer** is an AI-powered web app that lets users query a MySQL retail sales database using natural language.  
You simply ask questions like:

> "List the top 5 products by sales amount."

The app automatically converts your question into SQL, executes it, and displays the results — all in real-time.

---

## ⚙️ Features

✅ Query MySQL database using natural language  
✅ Auto-generate SQL with Google Gemini + LangChain  
✅ Instant execution and data visualization with Streamlit  
✅ Configurable database connection (user, password, host, db name)  
✅ Query history saved in the Streamlit session  
✅ Secure API key input via sidebar  

---

## 🧩 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Database:** MySQL  
- **AI Model:** Google Gemini (via LangChain)  
- **Libraries:** pandas, streamlit, langchain, sqlalchemy  

---

## 📁 Project Structure

```
app.py                  # Main Streamlit app
retail_sales_db.py      # Database and LLM chain functions
requirements.txt        # Dependencies list
```

---

## 🪄 How It Works

1. **Enter your Gemini API Key** in the sidebar.  
2. **Connect** to your MySQL database by entering credentials.  
3. Ask any **natural language question**, e.g. “Show total sales by category.”  
4. The app:
   - Uses Gemini + LangChain to generate SQL.
   - Executes it on your database.
   - Displays the results as a table.

---

## ⚡ Installation & Usage

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app
```bash
streamlit run app.py
```

### 4️⃣ Open in browser
Visit: [http://localhost:8501](http://localhost:8501)

---

## 🔑 Environment Variables

You can set your Gemini API key as an environment variable:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

## 🧠 Example Queries

- “Show total sales by product category.”  
- “List the top 10 customers by revenue.”  
- “Find average sales per month.”  
- “Which region has the highest sales?”  


## 👨‍💻 Author

**Retail Sales SQL Explorer** created by *Viishhnu*  
Exploring the intersection of **AI + Data Analytics + SQL Automation**.

---