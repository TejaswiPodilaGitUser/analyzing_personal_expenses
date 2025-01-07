# Analyzing Personal Expenses

<img width="1675" alt="image" src="https://github.com/user-attachments/assets/76990c1c-943d-4638-97a9-143eaf861dca" />

<img width="1691" alt="image" src="https://github.com/user-attachments/assets/a1a0d921-3907-430e-b544-87a1de8c7ef4" />

---
### 📥 Download & Setup
# Clone the repository using Git:
# git clone git@github.com:TejaswiPodilaGitUser/analyzing_personal_expenses.git
# cd analyzing_personal_expenses

### Setup Environment (Using Anaconda Navigator or Conda CLI)

# 1. Create a New Environment:
# conda create -n your_env_name python=3.9

# 2. Activate the Environment:
# conda activate your_env_name

# 3. Install Required Python Packages:
# pip install pandas seaborn numpy matplotlib streamlit plotly python-dotenv
# pip install mysql-connector-python
# pip install Faker
# pip install mplcursors
# pip install sqlalchemy
# pip install psutil
# pip install selenium
# pip install matplotlib reportlab
# pip install fpdf
# pip install bcrypt

### 📊 Database Setup

# 1. Configure Database Credentials
# Create a `.env` file in the project root and add the following details:
# DB_HOST=localhost
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_NAME=your_db_name

# 2. Grant Privileges to the User
# Log in to your MySQL server and run the following command:
# CREATE USER 'your_db_user'@'localhost' IDENTIFIED BY 'your_db_password';
# GRANT ALL PRIVILEGES ON your_db_name.* TO 'your_db_user'@'localhost';
# FLUSH PRIVILEGES;

# 3. Create Database Tables
# python scripts/create_tables.py

# 4. Populate Data in all tables
# python scripts/populate_data.py

# 5. Populate Expenses table data
# python scripts/populate_expenses.py

# 6. Populate Expenses table with random Null /blank data
# python scripts/populate_expenses_with_blanks.py

### 📝 Exploratory Data Analysis (EDA)

# Data Cleaning:
# Removed duplicates.
# Handled missing values.
# Converted data types to appropriate formats (e.g., dates to datetime).

# Descriptive Statistics:
# Calculated basic statistics (mean, median, mode, standard deviation) for numerical columns.
# Summarized categorical data.

# Data Visualization:
# Monthly Expenses: Visualized monthly expenses using bar charts and pie charts.
# Yearly Expenses: Visualized yearly expenses using bar charts and pie charts.
# Top Categories: Identified and visualized the top spending categories.
# Subcategory Breakdown: Detailed analysis of expenses by subcategories.
# Trends Over Time: Line charts to show spending trends over time.

# Insights Generation:
# Identified the highest and lowest spending categories.
# Analyzed spending patterns and trends.
# Provided insights into potential areas for cost-saving.

# Data Export:
# Exported cleaned and processed data to CSV for further analysis.

### 🚀 Run the Application
# Start the Streamlit application:
# streamlit run app/main.py

### 📚 Summary of Libraries Used
# Streamlit: For building interactive dashboards and displaying visual insights.
# Faker: To generate synthetic data for testing and populating the database.
# Matplotlib: For creating visualizations like bar charts and pie charts to represent expenses effectively.

# More Package Descriptions:
# pandas: Data manipulation and analysis library.
# seaborn: Statistical data visualization library built on Matplotlib.
# numpy: Numerical computations and array processing.
# plotly: Library for creating interactive charts and dashboards.
# python-dotenv: Loads environment variables from a `.env` file.
# mysql-connector-python: MySQL database connector for Python.
# mplcursors: Interactive cursor support for Matplotlib plots.
# sqlalchemy: SQL toolkit and Object Relational Mapper (ORM).
# psutil: Provides system and process utilities for resource monitoring.
# selenium: Automates web application testing and interaction.
# reportlab: PDF generation library for Python.
# fpdf: Lightweight library for PDF document generation.
# bcrypt: Library for password hashing and authentication.

### Charts Implemented
# 1. Pie Chart: Visualizes the distribution of monthly and yearly expenses based on selected filters.
# 2. Bar Chart: Compares monthly and yearly expense trends based on selected filters.
# 3. Donut Chart: Represents the proportional distribution of expense categories filtered by month and year.
# 4. Line Chart: Shows trends and patterns in expenses over time with monthly and yearly filters.
# 5. Scatter Chart: Displays relationships and correlations between expense categories and amounts over time.

### 💻 Contribution
# Feel free to fork this repository, raise issues, or submit pull requests.

### 📜 License
# This project is open source and licensed under the MIT License.
