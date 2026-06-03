# GenAI Prompt Engineering & Data Extraction

## Project Objective

This project demonstrates the power of Generative AI and Prompt Engineering using the Groq API with Llama models. It includes two major implementations:
1. **GenAI Data Extraction Project** - Converting messy text data into structured JSON using LLM
2. **Student Analytics System** - Complete analytics pipeline with database operations, visualizations, and ML predictions

The project helps to understand:
- Prompt Engineering techniques
- Working with Large Language Models (LLMs)
- Data extraction using GenAI
- Converting unstructured data to structured formats
- Database operations with SQLite
- Data visualization with Matplotlib
- Machine Learning with Random Forest

---

## Technologies Used

- **GenAI Frameworks**: Groq API, Llama 3.3-70B-Versatile
- **Data Processing**: Python, Pandas, NumPy
- **Database**: SQLite3
- **Visualization**: Matplotlib
- **Machine Learning**: Scikit-learn (Random Forest Regressor)
- **Environment**: Google Colab

---

## Project Folder Structure

```text
Day_06_GenAI_Prompt_Engineering
│
├── GenAI_Data_Extraction_Project.ipynb
├── Student_Analytics_System.ipynb
├── Student_Analytics_System1.ipynb
├── day_06_genai_promptengineering.py
├── student_performance.csv
└── README.md
```

---

## Files Description

### GenAI_Data_Extraction_Project.ipynb
GenAI-powered data extraction system that converts messy employee records (CSV format) into clean JSON structures. Demonstrates prompt engineering, JSON parsing, and DataFrame creation.

### Student_Analytics_System.ipynb
Complete student performance analytics system with:
- SQLite database creation and queries
- Data visualization (bar charts, scatter plots, pie charts)
- Random Forest model for programming score prediction
- Performance metrics calculation (MAE, R² Score)

### Student_Analytics_System1.ipynb
Alternative implementation of the student analytics system with enhanced visualizations.

### day_06_genai_promptengineering.py
Python script version of the GenAI prompt engineering implementation.

### student_performance.csv
Dataset containing student academic records with columns: student_id, name, age, gender, department, semester, scores, attendance, city, and admission year.

---

## Project 1: GenAI Data Extraction

### Input Data Format
```text
Ramesh Kumar,45000,Mumbai
Priya Nair,52000,Delhi
Ananya Das,38000,Kolkata
Arjun Singh,60000,Chennai
Sneha Patel,55000,Pune
```

### Output JSON Format
```json
{
  "name": "Ramesh Kumar",
  "salary": 45000,
  "city": "Mumbai"
}
```

### Key Features
- **LLM Integration**: Groq API with Llama 3.3-70B model
- **Prompt Engineering**: Crafted prompts for accurate JSON extraction
- **Data Cleaning**: Remove markdown formatting from LLM responses
- **DataFrame Creation**: Convert JSON to Pandas DataFrame
- **Analysis**: Calculate average, max, min salaries
- **Visualization**: Bar chart of employee salaries

### Prompt Engineering Techniques
1. **Clear Instructions**: Specify exact output format
2. **Examples**: Provide sample input-output pairs
3. **Constraints**: "Return ONLY raw JSON, Do NOT use markdown"
4. **Format Specification**: Define JSON structure explicitly

---

## Project 2: Student Analytics System

### Dataset Overview
- **Rows**: 30 students
- **Columns**: 13 attributes
- **Departments**: Computer Science, Electronics, Mechanical, Civil

### Database Operations (SQLite)

```sql
-- Average Programming Score by Department
SELECT department, 
       AVG(programming_score) AS avg_score
FROM students
GROUP BY department;
```

### Results by Department
| Department | Average Programming Score |
|------------|--------------------------|
| Computer Science | 89.23 |
| Electronics | 61.50 |
| Mechanical | 49.33 |
| Civil | 40.60 |

### Visualizations Created
1. **Bar Chart**: Average Programming Score by Department
2. **Scatter Plot**: Attendance vs Programming Score
3. **Pie Chart**: Gender Distribution (53.3% Male, 46.7% Female)

### Machine Learning Model

**Algorithm**: Random Forest Regressor
- **Features**: math_score, english_score, attendance_percentage
- **Target**: programming_score
- **Train-Test Split**: 80-20
- **Estimators**: 100 trees

**Performance Metrics**:
- **MAE (Mean Absolute Error)**: 10.19
- **R² Score**: 0.6292 (62.92% variance explained)

---

## GenAI Workflow

### 1. Setup Groq API
```python
from groq import Groq

API_KEY = "your_api_key_here"
client = Groq(api_key=API_KEY)
MODEL = "llama-3.3-70b-versatile"
```

### 2. Create LLM Query Function
```python
def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### 3. Craft Effective Prompt
```python
prompt = """
Convert this employee record into JSON.

Input:
Ramesh Kumar,45000,Mumbai

Return ONLY raw JSON.
Do NOT use markdown.
Do NOT use ```json.
"""
```

### 4. Parse and Process Response
```python
result = ask_llm(prompt)
clean_result = result.strip()
parsed_data = json.loads(clean_result)
```

---

## Student Analytics Workflow

### 1. Data Loading
```python
df = pd.read_csv("student_performance.csv")
```

### 2. Database Creation
```python
conn = sqlite3.connect("student.db")
df.to_sql("students", conn, if_exists="replace", index=False)
```

### 3. SQL Analysis
```python
query = """
SELECT department, AVG(programming_score) AS avg_score
FROM students GROUP BY department
"""
result = pd.read_sql(query, conn)
```

### 4. Visualization
```python
dept_avg.plot(kind="bar", figsize=(8,5))
plt.title("Average Programming Score by Department")
plt.show()
```

### 5. ML Prediction
```python
X = df[["math_score", "english_score", "attendance_percentage"]]
y = df["programming_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
predictions = rf_model.predict(X_test)
```

---

## Key Insights

### From GenAI Data Extraction
- **Salary Range**: ₹38,000 - ₹60,000
- **Average Salary**: ₹50,000
- **Prompt Engineering**: Reduces post-processing by 80%
- **Accuracy**: 100% JSON structure with proper constraints

### From Student Analytics
1. **Department Performance**:
   - Computer Science students have highest programming scores (89.23)
   - Civil Engineering students need more programming support (40.60)

2. **Attendance Impact**:
   - Positive correlation between attendance and programming scores
   - Students with >85% attendance score significantly higher

3. **Gender Distribution**:
   - Nearly balanced (53.3% Male, 46.7% Female)
   - No significant gender gap in performance

4. **Model Performance**:
   - Predicts programming scores with MAE of 10.19 points
   - 62.92% of score variance explained by the model

---

## Installation & Setup

### Step 1: Install Required Libraries
```bash
pip install groq pandas matplotlib scikit-learn
```

### Step 2: Obtain Groq API Key
1. Visit [Groq Cloud Console](https://console.groq.com)
2. Create an account
3. Generate API key
4. Replace in code: `API_KEY = "your_api_key_here"`

### Step 3: Run in Google Colab
1. Upload notebooks to Google Colab
2. Upload `student_performance.csv` when prompted
3. Execute cells sequentially
4. View results and visualizations

---

## Prompt Engineering Best Practices

### 1. Be Specific
❌ Bad: "Convert to JSON"
✅ Good: "Convert this employee record into JSON with fields: name, salary, city"

### 2. Provide Examples
```
Example:
Input: John Doe,50000,New York
Output: {"name":"John Doe","salary":50000,"city":"New York"}
```

### 3. Set Constraints
- "Return ONLY raw JSON"
- "Do NOT use markdown formatting"
- "Do NOT include explanations"

### 4. Specify Format
- Define exact JSON structure
- Specify data types (string, integer)
- Indicate required vs optional fields

---

## Learning Outcomes

Through this project, you learned:

### GenAI & Prompt Engineering
- Integrating LLM APIs (Groq) in Python
- Crafting effective prompts for data extraction
- Handling LLM responses and parsing JSON
- Converting unstructured to structured data
- Managing API keys securely

### Data Analytics
- SQLite database operations in Python
- SQL queries for aggregation and grouping
- Data visualization with Matplotlib
- Statistical analysis with Pandas

### Machine Learning
- Random Forest Regressor implementation
- Train-test split methodology
- Model evaluation metrics (MAE, R²)
- Feature selection for prediction

### Software Engineering
- Jupyter Notebook development
- Code organization and documentation
- Error handling and data validation
- Reproducible data science workflows

---

## Future Enhancements

1. **Advanced Prompt Engineering**:
   - Few-shot learning with multiple examples
   - Chain-of-thought prompting
   - Self-consistency checks

2. **Expanded Analytics**:
   - Time series analysis of student progress
   - Clustering students by performance patterns
   - Predictive analytics for at-risk students

3. **Model Improvements**:
   - Hyperparameter tuning for Random Forest
   - Try other algorithms (XGBoost, Neural Networks)
   - Feature engineering (interaction terms)

4. **Deployment**:
   - Create Streamlit web app
   - API endpoints with Flask/FastAPI
   - Real-time predictions

---

## Common Issues & Solutions

### Issue 1: Groq API Key Error
**Error**: `Invalid API key`
**Solution**: Ensure API key is correctly copied and has no extra spaces

### Issue 2: JSON Parsing Error
**Error**: `json.decoder.JSONDecodeError`
**Solution**: Enhanced prompt to explicitly forbid markdown formatting

### Issue 3: Model Overfitting
**Error**: High training accuracy, low test accuracy
**Solution**: Use cross-validation and regularization

### Issue 4: Missing Data
**Error**: `KeyError` when accessing columns
**Solution**: Check column names with `df.columns` before accessing

---

## Project Results Summary

### GenAI Data Extraction
✅ Successfully converted 5 messy employee records to clean JSON
✅ Created DataFrame with proper data types
✅ Generated salary analysis visualization
✅ Demonstrated effective prompt engineering

### Student Analytics System
✅ Created SQLite database with 30 student records
✅ Executed complex SQL aggregation queries
✅ Generated 3 different visualization types
✅ Trained ML model with 62.92% R² score
✅ Predicted programming scores with MAE of 10.19

---

## Technologies Deep Dive

### Groq Cloud
- **Speed**: 10x faster inference than traditional LLM APIs
- **Model**: Llama 3.3-70B-Versatile (70 billion parameters)
- **Advantages**: Low latency, high throughput, cost-effective

### Random Forest Regressor
- **Ensemble Method**: Combines multiple decision trees
- **Advantages**: Handles non-linear relationships, robust to outliers
- **Hyperparameters**: n_estimators=100, random_state=42

### SQLite
- **Lightweight**: No separate server required
- **Portable**: Single file database
- **SQL Compliant**: Standard SQL syntax

---

## References & Resources

### Documentation
- [Groq API Documentation](https://console.groq.com/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

### Prompt Engineering
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)

### Machine Learning
- [Random Forest Explained](https://scikit-learn.org/stable/modules/ensemble.html#forest)
- [Model Evaluation Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)

---

## Conclusion

This project successfully demonstrates the integration of GenAI capabilities with traditional data analytics and machine learning workflows. By combining:
- **GenAI** for intelligent data extraction
- **SQL** for structured queries
- **Pandas** for data manipulation
- **Matplotlib** for visualization
- **Scikit-learn** for predictions

We created a comprehensive analytics system that showcases modern data science practices.

---

## Contact & Contribution

**Author**: Aman Karn  
**Institution**: Sri Eshwar College of Engineering  
**Program**: Third Year CSE Student  
