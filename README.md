# Analyzing Personal Expenses

<img width="1505" alt="image" src="https://github.com/user-attachments/assets/8edfaf2b-9300-4008-afb7-9d5f393d80a5" />

<img width="1495" alt="image" src="https://github.com/user-attachments/assets/25befc08-a42f-44b9-a9e7-635529a44371" />

<img width="1468" alt="image" src="https://github.com/user-attachments/assets/1477d30e-0eb9-4512-8b70-e1b504f8a41d" />



---

## 📥 Download & Setup
Clone the repository using Git:
```bash
git clone git@github.com:TejaswiPodilaGitUser/analyzing_personal_expenses.git
cd analyzing_personal_expenses
```

### Setup Environment (Using Anaconda Navigator or Conda CLI)

1. Create a New Environment:
```bash
conda create -n your_env_name python=3.9
```
(Replace `your_env_name` with any preferred environment name.)

2. Activate the Environment:
```bash
conda activate your_env_name
```

3. Install Required Python Packages:
```bash
pip install pandas seaborn numpy matplotlib streamlit plotly python-dotenv
pip install mysql-connector-python
pip install Faker
pip install mplcursors
pip install sqlalchemy
pip install psutil
pip install selenium
pip install matplotlib reportlab
pip install fpdf
pip install bcrypt
```

## 📊 Database Setup

### 1. Configure Database Credentials
Create a `.env` file in the project root and add the following details:
```env
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```
(Replace `your_db_user`, `your_db_password`, and `your_db_name` with your own database details.)

### 2. Grant Privileges to the User
Log in to your MySQL server and run the following command:
```sql
CREATE USER 'your_db_user'@'localhost' IDENTIFIED BY 'your_db_password';
GRANT ALL PRIVILEGES ON your_db_name.* TO 'your_db_user'@'localhost';
FLUSH PRIVILEGES;
```

If any issues are faced while connecting to the database:
- Verify that the MySQL server is running.
- Ensure that credentials in the `.env` file are correct.
- Check if the MySQL user has the required privileges.
- Review MySQL error logs for more details.

### 3. Create Database Tables
```bash
python scripts/create_tables.py
```

### 4. Populate Data in all tables
```bash
python scripts/populate_data.py
```

### 5. Populate Expenses table data
```bash
python scripts/populate_expenses.py
```

### 6. Populate Expenses table with random Null /blank data
```bash
python scripts/populate_expenses_with_blanks.py
```
## Exploratory Data Analysis (EDA) Overview

The Exploratory Data Analysis (EDA) for this project focuses on understanding the structure and patterns within the personal expenses dataset. The following steps were performed:

### 1. Data Cleaning

The data cleaning process ensures the dataset is accurate and ready for analysis. It involves handling missing values, standardizing date formats, and ensuring consistency in numerical data. Key steps include:

1. **Handling Missing Values**: Missing values in categorical and numerical data are filled with the mode and mean, respectively, while critical missing data is dropped.
2. **Date Formatting**: Dates are standardized into a consistent format for easier analysis.
3. **Validating Amounts**: Non-numeric values in the `amount_paid` column are handled and converted to valid numeric values.

These steps improve the quality and consistency of the dataset, making it suitable for meaningful insights and visualizations.

### 2. Descriptive Statistics

- **Numerical Data**: Basic statistics (mean, median, standard deviation) were calculated to understand the distribution and variability of the data.
- **Categorical Data**: Frequency analysis was conducted to identify the most common categories and subcategories.

### 3. Data Visualization

- **Expense Trends**: Monthly and yearly expenses were visualized using **pie**, **bar**, **line**, **scatter**, and **donut** plots to reveal spending patterns.
- **Category Breakdown**: A **horizontal bar chart** was created to explore the distribution of expenses across various categories.
- **Payment Mode Breakdown**: A **bar chart** visualizes payment mode distribution to analyze transaction types.

### 4. Insights Generation

Key insights were derived from the data, including:
- **Highest and Lowest Spending Categories**: The top categories with the highest and lowest expenditures.
- **Max and Min Payment Methods**: The most and least frequently used payment methods.

### 5. Data Export (Removed)

The data export option was removed in this version to streamline the user experience.

## Features

- **User Selection**: Users can select different individuals to analyze their personal expenses.
- **Visualization Options**: Choose between **monthly** and **yearly** visualizations of expenses.
- **Detailed Category Breakdown**: Drill down into specific categories and subcategories to gain deeper insights.
- **Subcategory Expenses for Category**: Based on the selected category, all subcategories will be displayed with their total expenses.
- **Payment Mode Insights**: View insights into the most frequently used payment methods, such as **Online**, **Cash**, **Credit Card**, etc.
  
## 🚀 Run the Application
Start the Streamlit application:
```bash
streamlit run app/main.py
```

## 📚 Summary of Libraries Used

- Streamlit: For building interactive dashboards and displaying visual insights.
- Faker: To generate synthetic data for testing and populating the database.
- Matplotlib: For creating visualizations like bar charts and pie charts to represent expenses effectively.

More Package Descriptions:
- pandas: Data manipulation and analysis library.
- seaborn: Statistical data visualization library built on Matplotlib.
- numpy: Numerical computations and array processing.
- plotly: Library for creating interactive charts and dashboards.
- python-dotenv: Loads environment variables from a `.env` file.
- mysql-connector-python: MySQL database connector for Python.
- mplcursors: Interactive cursor support for Matplotlib plots.
- sqlalchemy: SQL toolkit and Object Relational Mapper (ORM).
- psutil: Provides system and process utilities for resource monitoring.
- selenium: Automates web application testing and interaction.
- reportlab: PDF generation library for Python.
- fpdf: Lightweight library for PDF document generation.
- bcrypt: Library for password hashing and authentication.

## Charts Implemented

1. Pie Chart: Visualizes the distribution of monthly and yearly expenses based on selected filters.
2. Bar Chart: Compares monthly and yearly expense trends based on selected filters.
3. Donut Chart: Represents the proportional distribution of expense categories filtered by month and year.
4. Line Chart: Shows trends and patterns in expenses over time with monthly and yearly filters.
5. Scatter Chart: Displays relationships and correlations between expense categories and amounts over time.

## 💻 Contribution
Feel free to fork this repository, raise issues, or submit pull requests.

## 📜 License
This project is open source and licensed under the MIT License.

---
Happy Analyzing! 🚀📊

