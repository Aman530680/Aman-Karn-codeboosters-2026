# Big Data, PySpark & Architecture

## Project Objective

This mini project is created using Python, PySpark, and Pandas to analyze large-scale sales data using Apache Spark and explore housing data using Pandas.

The project helps to understand:
- Big Data processing using PySpark
- Medallion Architecture (Bronze, Silver, Gold layers)
- Sales data analysis using Spark SQL operations
- Housing dataset analysis using Pandas
- Linear Regression concepts

---

## Technologies Used

- Python
- PySpark
- Pandas
- Matplotlib
- Google Colab

---

## Project Folder Structure

```text
Day_04_BigData_PySpark_Architecture
│
├── Day_04_PySpark_Basics_Sales_Data.ipynb
├── Day_04_Housing_Data_Analysis.ipynb
├── Day_04_Linear_Regression_Height_Weight (1).ipynb
├── Housing.csv
└── README.md
```

---

## Files Description

### Day_04_PySpark_Basics_Sales_Data.ipynb
Contains PySpark basics and Medallion Architecture implementation using large sales data — SparkSession setup, DataFrame operations, filtering, groupBy, aggregations, and Bronze/Silver/Gold layers.

### Day_04_Housing_Data_Analysis.ipynb
Contains housing dataset analysis using Pandas — data loading, shape, columns, missing values, duplicates, statistical analysis, price analysis, and visualization.

### Day_04_Linear_Regression_Height_Weight (1).ipynb
Contains Linear Regression implementation using height and weight data.

### Housing.csv
Dataset file containing housing details and prices.

### README.md
Project documentation file.

---

## Dataset Columns

### large_sales_data.csv (PySpark)

| Column | Description |
|--------|-------------|
| order_id | Unique order identifier |
| customer_name | Customer full name |
| product | Product name |
| category | Electronics / Accessories |
| quantity | Number of units ordered |
| unit_price | Price per unit in INR |
| revenue | Total revenue (quantity × unit_price) |
| order_date | Date of order |
| city | Customer city |
| region | North / South / East / West |
| sales_rep | Sales representative name |
| payment_method | UPI / Credit Card / Net Banking / Cash on Delivery |
| order_status | Delivered / Shipped / Processing / Cancelled |

### Housing.csv (Pandas)

| Column | Description |
|--------|-------------|
| price | House price |
| area | Area in square feet |
| bedrooms | Number of bedrooms |
| bathrooms | Number of bathrooms |
| stories | Number of stories |
| mainroad | Main road access (yes/no) |
| guestroom | Guest room available (yes/no) |
| basement | Basement available (yes/no) |
| hotwaterheating | Hot water heating (yes/no) |
| airconditioning | Air conditioning (yes/no) |
| parking | Number of parking spaces |
| prefarea | Preferred area (yes/no) |
| furnishingstatus | furnished / semi-furnished / unfurnished |

---

## Features of the Project

### PySpark Basics — Sales Data
- SparkSession setup
- Load CSV into Spark DataFrame
- Show schema and columns
- Filter rows (revenue > 100000)
- GroupBy region — count and total revenue
- GroupBy product — order count
- GroupBy payment method — count
- OrderBy revenue descending
- GroupBy order status — count

### Medallion Architecture
- **Bronze Layer** — Raw data loaded from CSV (5000 rows)
- **Silver Layer** — Cleaned data (drop duplicates, fill nulls)
- **Gold Layer** — Business-ready aggregated data (total revenue by region)

### Housing Data Analysis
- Dataset overview (545 rows, 13 columns)
- Missing values check — no missing values
- Duplicate rows check — no duplicates
- Statistical analysis using `describe()`
- Correlation matrix (numeric columns)
- Price analysis (average, max, min)
- House price distribution histogram

---

## Key Results

### PySpark Sales Analysis
| Region | Total Revenue (INR) |
|--------|---------------------|
| West | 19,82,75,600 |
| South | 14,71,45,900 |
| North | 9,98,78,400 |
| East | 5,05,47,700 |

### Top Product by Orders
| Product | Orders |
|---------|--------|
| Webcam | 532 |
| Tablet | 532 |
| USB Hub | 527 |
| Laptop | 502 |

### Housing Data Analysis
| Metric | Value |
|--------|-------|
| Total Houses | 545 |
| Average Price | ₹47,66,729 |
| Maximum Price | ₹1,33,00,000 |
| Minimum Price | ₹17,50,000 |

---

## How to Run the Project

### Step 1
Open Google Colab

### Step 2
Install PySpark

```python
!pip install pyspark --quiet
```

### Step 3
Import required libraries

```python
from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt
```

### Step 4
Upload the dataset files and run all notebook cells

---

## Learning Outcomes

Through this project, we learned:
- Setting up and using Apache Spark with PySpark
- Loading and exploring large datasets with Spark DataFrames
- Filtering, grouping, and aggregating data using PySpark
- Medallion Architecture (Bronze → Silver → Gold)
- Housing data analysis using Pandas
- Correlation analysis between features
- Data visualization using Matplotlib
- Linear Regression concepts

---

## Author

Aman Karn

Third Year CSE Student  
Sri Eshwar College of Engineering
