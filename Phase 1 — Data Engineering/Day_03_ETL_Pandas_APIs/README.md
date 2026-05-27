# Day 03 — ETL, Pandas & APIs

## Project Objective

This mini project is created using Python, Pandas, and REST APIs to build an ETL (Extract, Transform, Load) pipeline on messy sales data and fetch live weather data using the OpenWeatherMap API.

The project helps to understand:
- ETL pipeline concepts (Extract, Transform, Load)
- Data cleaning and transformation using Pandas
- Handling missing values, duplicates, and inconsistent data
- Date parsing and feature engineering
- Revenue calculation and business analysis
- Fetching live data from REST APIs
- Saving cleaned data to CSV

---

## Technologies Used

- Python
- Pandas
- Requests (API calls)
- OpenWeatherMap API
- VS Code / Google Colab

---

## Project Folder Structure

```text
Day_03_ETL_Pandas_APIs
│
├── class_practice3.ipynb
├── Practice_Questions_3.ipynb
├── Weather_Data_ETL_Project.ipynb
├── messy_sales_data.csv
└── README.md
```

---

## Files Description

### class_practice3.ipynb
Contains the full ETL pipeline on `messy_sales_data.csv` — data loading, quality diagnosis, cleaning, transformation, revenue analysis, and API configuration.

### Practice_Questions_3.ipynb
Contains practice questions based on ETL concepts, data cleaning, and API usage.

### Weather_Data_ETL_Project.ipynb
Main mini project notebook — fetches live weather data for 10 Indian cities using the OpenWeatherMap API and saves it as a CSV file.

### messy_sales_data.csv
Raw dataset with intentional data quality issues — missing values, inconsistent casing, wrong categories, and mixed date formats.

### README.md
Project documentation file.

---

## Dataset — `messy_sales_data.csv`

| Column | Description |
|--------|-------------|
| order_id | Unique order identifier (1001–1030) |
| customer_name | Customer full name (has casing issues & nulls) |
| product | Product name (Laptop, Monitor, Keyboard, etc.) |
| category | Electronics / Accessories (has wrong entries) |
| quantity | Number of units ordered (has nulls) |
| unit_price | Price per unit in INR |
| order_date | Order date (has mixed formats) |
| city | Customer city |
| sales_rep | Sales representative name |

---

## ETL Pipeline — `class_practice3.ipynb`

### EXTRACT
- Loaded `messy_sales_data.csv` — 30 rows, 9 columns

### TRANSFORM — Data Quality Issues Found & Fixed

| Issue | Details | Fix Applied |
|-------|---------|-------------|
| Missing values | customer_name: 2, product: 1, category: 1, quantity: 3 | Identified and flagged |
| Duplicate rows | 0 duplicates found | No action needed |
| Inconsistent casing | `AMIT VERMA`, `kiran mehta` | Applied `.str.title()` |
| Wrong category | Keyboard tagged as Electronics | Fixed to Accessories |
| Mixed date formats | `2024-01-05` and `07-01-2024` mixed | Parsed with `pd.to_datetime()` |
| Date feature engineering | Extracted year, month, month_name | New columns added |
| Revenue calculation | `quantity × unit_price` | New `revenue` column added |

### LOAD
- Cleaned data saved to `clean_sales_data.csv` — 30 rows, 13 columns

---

## Revenue Analysis Results

### Revenue by Product
| Product | Revenue (INR) |
|---------|--------------|
| Laptop | 4,50,000 |
| Monitor | 1,10,000 |
| Headphones | 28,000 |
| Mouse | 20,800 |
| Keyboard | 20,400 |
| USB Hub | 19,800 |
| Webcam | 15,000 |

### Category Summary
| Category | Total Revenue | Avg Order Value | Orders | Products |
|----------|--------------|-----------------|--------|----------|
| Electronics | 5,59,000 | 43,000 | 15 | 3 |
| Accessories | 76,000 | 5,846 | 14 | 4 |

**Total Revenue: ₹6,79,000**

---

## Weather Data ETL Project — `Weather_Data_ETL_Project.ipynb`

### What it does
- Connects to the **OpenWeatherMap API**
- Fetches live weather data for **10 Indian cities**
- Extracts: City, Temperature (°C), Humidity (%), Weather description
- Saves the result to `weather_data.csv`

### Cities Covered
Delhi, Mumbai, Kolkata, Chennai, Bangalore, Hyderabad, Ahmedabad, Pune, Jaipur, Lucknow

### Sample Output
| City | Temperature (°C) | Humidity (%) | Weather |
|------|-----------------|--------------|---------|
| Delhi | 39.05 | 17 | haze |
| Mumbai | 30.99 | 70 | haze |
| Kolkata | 25.97 | 89 | thunderstorm |
| Chennai | 32.20 | 65 | haze |
| Bengaluru | 25.67 | 75 | scattered clouds |

---

## How to Run the Project

### Step 1
Open the project folder in VS Code and select the `.venv` Python kernel

### Step 2
Install required libraries

```bash
pip install pandas requests
```

### Step 3
Import required libraries

```python
import pandas as pd
import requests
```

### Step 4
For ETL pipeline — run `class_practice3.ipynb` cells in order

### Step 5
For Weather API project — add your API key and run `Weather_Data_ETL_Project.ipynb`

```python
api_key = "YOUR_API_KEY_HERE"  # Get free key from openweathermap.org
```

> **Note:** The `google.colab` import cells can be skipped — all files are already in the same folder locally.

---

## Learning Outcomes

Through this project, we learned:
- ETL pipeline concepts (Extract, Transform, Load)
- Detecting and fixing data quality issues
- Handling missing values and duplicates
- Standardizing text data with Pandas string methods
- Parsing mixed date formats with `pd.to_datetime()`
- Feature engineering (revenue, year, month columns)
- Groupby aggregations for business analysis
- Making REST API calls using the `requests` library
- Parsing JSON responses from APIs
- Saving DataFrames to CSV files

---

## Author

Aman Karn

Third Year CSE Student  
Sri Eshwar College of Engineering
