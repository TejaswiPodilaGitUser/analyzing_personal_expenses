# Analyzing Personal Expenses

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

## 🧹 Data Cleaning and Filtering

- Cleaning:
   - Removed duplicate records.
   - Handled null and blank values in expense records.
   - Standardized date formats and currency values.
   - Validated expense categories and subcategories.

- Filtering:
   - Filtered data by year, month, and expense category.
   - Enabled dynamic filtering through Streamlit UI components.

## 🚀 Run the Application
Start the Streamlit application:
```bash
streamlit run app/main.py
```

## 📚 Summary of Libraries Used

1. Streamlit: For building interactive dashboards and displaying visual insights.
2. Faker: To generate synthetic data for testing and populating the database.
3. Matplotlib: For creating visualizations like bar charts and pie charts to represent expenses effectively.

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

