# Day 9: AI Agents - Text to SQL

This project demonstrates building an AI-powered Text-to-SQL agent that converts natural language questions into SQL queries using Groq's LLM.

## Overview

The AI Agent takes a user's natural language question, generates a corresponding SQL query using the Groq LLM, executes it on a SQLite database, and returns the results as a DataFrame.

## Prerequisites

- Python 3.x
- Groq API Key
- Required packages:
  ```bash
  pip install groq pandas
  ```

## Project Structure

- **Class_Practice9.ipynb** - Main Jupyter notebook with the complete implementation
- **college.db** - SQLite database with student data
- **README.md** - This documentation file

## Database Schema

The project uses a SQLite database (`college.db`) with a `students` table:

| Column | Data Type | Description |
|--------|-----------|-------------|
| student_id | INTEGER | Primary key |
| name | TEXT | Student name |
| age | INTEGER | Student age |
| gender | TEXT | Student gender |
| subject | TEXT | Subject name |
| marks | INTEGER | Marks scored |
| attendance | INTEGER | Attendance percentage |
| grade | TEXT | Grade (A, B, C, D) |

## How It Works

### 1. Setup Groq Client
```python
from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "your_api_key"
client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.1-8b-instant"
```

### 2. Get Database Schema
```python
def get_schema(conn, table_name="students"):
    """Retrieve table structure (columns and data types)"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    # Returns formatted schema string
```

### 3. Generate SQL Query
```python
def generate_sql_query(user_question, system_prompt, client, model):
    """Convert natural language to SQL using Groq LLM"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()
```

### 4. Execute SQL Query
```python
def execute_sql(sql_query, conn):
    """Execute generated SQL and return results as DataFrame"""
    results_df = pd.read_sql_query(clean_sql_query, conn)
    return results_df
```

## Usage Example

```python
import sqlite3

# Connect to database
conn = sqlite3.connect("college.db")

# Define system prompt with schema
system_prompt = f"""You are an expert SQL assistant.
Schema for table 'students':
- student_id (INTEGER, Primary Key)
- name (TEXT)
- age (INTEGER)
- gender (TEXT)
- subject (TEXT)
- marks (INTEGER)
- attendance (INTEGER)
- grade (TEXT)

Rules:
1. Generate ONLY valid SQLite SQL queries
2. Do not include explanations - only raw SQL
3. Do not use markdown code blocks"""

# Ask a question
user_question = "What are the names of students who have a grade of 'A' and scored more than 90 marks?"

# Generate and execute SQL
sql_query = generate_sql_query(user_question, system_prompt, client, MODEL)
results = execute_sql(sql_query, conn)

print(results)
conn.close()
```

## Sample Questions

Try these questions with the agent:
- "Show me all students with grade 'A'"
- "List students who scored more than 85 marks"
- "Find students with attendance above 90%"
- "Show male students studying Mathematics"
- "Count students by grade"

## Key Features

- **Natural Language to SQL**: Converts plain English questions to SQL queries
- **Schema-Aware**: Uses database schema information for accurate query generation
- **SQLite Integration**: Works with local SQLite databases
- **Pandas Integration**: Returns results as DataFrames for easy data manipulation

## Error Handling

The system handles:
- Invalid API keys (401 errors)
- SQL execution errors
- Empty result sets

## Model Used

- **Model**: `llama-3.1-8b-instant`
- **Provider**: Groq
- **Temperature**: 0.0 (deterministic output)

## Notes

- Ensure your Groq API key is valid and has sufficient quota
- The system prompt must include the database schema for accurate SQL generation
- Generated SQL queries are validated before execution