# Analyzing Personal Expenses

## 📥 Download & Setup
Clone the repository using Git:
```bash
git clone git@github.com:TejaswiPodilaGitUser/analyzing_personal_expenses.git
cd analyzing_personal_expenses
```

## 📊 Database Setup
1. **Configure Database Credentials:**
Create a `.env` file in the project root and add the following details:
```env
DB_HOST=localhost
DB_USER=Sample_db_user
DB_PASSWORD=Sample_db_user
DB_NAME=Sample_db
```

2. **Create Database Tables:**
```bash
python scripts/create_tables.py
```

3. **Populate Data:**
```bash
python scripts/populate_data.py
```

4. **Populate Expenses:**
```bash
python scripts/populate_expenses.py
```

5. **Populate Expenses with Blanks:**
```bash
python scripts/populate_expenses_with_blanks.py
```

## 🚀 Run the Application
Start the Streamlit application:
```bash
streamlit run app/main.py
```

## 📚 Summary of Libraries Used

- **Streamlit:** For building interactive dashboards and displaying visual insights.
- **Faker:** To generate synthetic data for testing and populating the database.
- **Matplotlib:** For creating visualizations like bar charts and pie charts to represent expenses effectively.

## 📈 Charts Implemented
- **Pie Chart:** Visualizes the distribution of monthly and yearly expenses.
- **Bar Chart:** Compares monthly and yearly expense trends.

## 💻 Contribution
Feel free to fork this repository, raise issues, or submit pull requests.

## 📜 License
This project is open source and licensed under the MIT License.

---
Happy Analyzing! 🚀📊✨

