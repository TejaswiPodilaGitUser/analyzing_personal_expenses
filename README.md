Analyzing Personal Expenses

📥 Download & Setup

Clone the repository using Git:

git clone git@github.com:TejaswiPodilaGitUser/analyzing_personal_expenses.git
cd analyzing_personal_expenses

📊 Database Setup

Configure Database Credentials:
Create a .env file in the project root and add the following details:

DB_HOST=localhost
DB_USER=Sample_db_user
DB_PASSWORD=Sample_db_user
DB_NAME=Sample_db

Create Database Tables:

python scripts/create_tables.py

Populate Data:

python scripts/populate_data.py

Populate Expenses:

python scripts/populate_expenses.py

Populate Expenses with Blanks:

python scripts/populate_expenses_with_blanks.py

🚀 Run the Application

Start the Streamlit application:

streamlit run app/main.py

📚 Summary of Libraries Used

Streamlit: For building interactive dashboards and displaying visual insights.

Faker: To generate synthetic data for testing and populating the database.

Matplotlib: For creating visualizations like bar charts and pie charts to represent expenses effectively.

📈 Charts Implemented

Pie Chart: Visualizes the distribution of monthly and yearly expenses.

Bar Chart: Compares monthly and yearly expense trends.

💻 Contribution

Feel free to fork this repository, raise issues, or submit pull requests.

📜 License

This project is open source and licensed under the MIT License.

Happy Analyzing! 🚀📊✨

