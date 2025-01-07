import streamlit as st
import pandas as pd
import sys
import os
import decimal

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.ui.data_visualization import DataVisualization
from backend.database.db_operations import DatabaseOperations
from utils.static_expense_data import MONTHS, MESSAGES
import frontend.ui.sidebar as sidebar
from scripts.static_data import CHART_TYPES
from backend.data_cleaner import DataCleaner
from frontend.ui.expense_summary_insights import ExpenseSummaryInsights
from frontend.ui.data_insights import get_insights
from frontend.ui.payment_mode_chart import PaymentModeChart
from frontend.ui.headings import Heading
from frontend.ui.bar_chart import plot_bar_chart,plot_bar_chart_payment
from frontend.ui.payment_insights import PaymentModesInsights
from frontend.ui.get_payment_mode_insights import get_payment_mode_insights


def main():
    """Main function to run the Expense Tracker Streamlit App."""
    st.set_page_config(layout="wide")

    # Initialize default variables
    insights = {}
    top_10_df = pd.DataFrame()

    # Initialize DatabaseOperations instance
    db_ops = DatabaseOperations()
    users = db_ops.fetch_users()

    # Sidebar: User and Filter Selections
    user_id, visualization_type, chart_type, selected_month, selected_year, detailed_view_category = sidebar.display_sidebar(users)

    # Fetch User Data for the year
    dv = DataVisualization(user_id=user_id)
    df = dv.get_user_expenses(user_id=user_id, selected_year=selected_year, selected_month=selected_month)

    if df.empty:
        st.warning(MESSAGES["no_user_data"])
        return

    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
    df['expense_year'] = df['expense_date'].dt.year
    df['expense_month'] = df['expense_date'].dt.strftime('%B')

    # Fetch categories and subcategories dynamically
    categories_df = db_ops.fetch_categories(user_id=user_id, selected_year=selected_year, selected_month=selected_month)
    subcategories_df = db_ops.fetch_subcategories(user_id=user_id, selected_year=selected_year, selected_month=selected_month)
    payment_mode_df=db_ops.fetch_payment_mode_counts(user_id=user_id, selected_year=selected_year, selected_month=selected_month)

    # Data Cleaning
    cleaner = DataCleaner(df, categories_df, subcategories_df)
    try:
        cleaned_df = cleaner.clean_data()
    except KeyError as e:
        st.error(f"Data Cleaning Error: {e}")
        st.stop()

    # Ensure 'amount_paid' column is of type float before aggregation
    cleaned_df['amount_paid'] = cleaned_df['amount_paid'].apply(lambda x: float(x) if isinstance(x, (int, float, decimal.Decimal)) else x)

    # Monthly Visualization
    if visualization_type == "Monthly":
        selected_year = selected_year or st.selectbox("Select Year", sorted(df['expense_year'].unique()), key="year")
        selected_month = selected_month or st.selectbox("Select Month", MONTHS, key="month")

        filtered_df = cleaned_df[
            (cleaned_df['expense_month'] == selected_month) &
            (cleaned_df['expense_year'] == int(selected_year))
        ]

        if filtered_df.empty:
            st.warning(MESSAGES["no_month_data"].format(month=selected_month, year=selected_year))
        else:
            heading = Heading(f"📊 Monthly Expenses Overview for {selected_month} {selected_year}")
            heading.display_centered()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 💰 Top 10 Spending Categories")
                top_10_df = (
                    filtered_df.groupby('category_name', as_index=False)
                    .agg(total_amount=('amount_paid', 'sum'))
                )
                top_10_df = top_10_df[top_10_df['total_amount'] > 0]
                top_10_df = top_10_df.sort_values(by='total_amount', ascending=False).head(10)
                top_10_df['total_amount'] = top_10_df['total_amount'].round(2)
                st.dataframe(top_10_df)

            with col2:
                if chart_type in CHART_TYPES:
                    filtered_chart_df = filtered_df[filtered_df['amount_paid'] > 0]
                    dv.display_monthly_expenses(filtered_chart_df, selected_year, selected_month, chart_type)
                else:
                    st.warning(f"Invalid chart type selected: {chart_type}")

            insights = get_insights(filtered_df)

    # Yearly Visualization
    elif visualization_type == "Yearly":
        selected_year = selected_year or st.selectbox("Select Year", sorted(df['expense_year'].unique()), key="year")
        filtered_df = cleaned_df[cleaned_df['expense_year'] == int(selected_year)]

        if filtered_df.empty:
            st.warning(MESSAGES["no_year_data"].format(year=selected_year))
        else:
            heading = Heading(f"📊 Yearly Expenses Overview for {selected_year}")
            heading.display_centered()
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 💰 Top 10 Yearly Expenses")
                yearly_expenses_df = (
                    filtered_df.groupby('category_name', as_index=False)
                    .agg(total_amount=('amount_paid', 'sum'))
                )
                yearly_expenses_df = yearly_expenses_df[yearly_expenses_df['total_amount'] > 0]
                yearly_expenses_df = yearly_expenses_df.sort_values(by='total_amount', ascending=False).head(10)
                yearly_expenses_df['total_amount'] = yearly_expenses_df['total_amount'].round(2)
                st.dataframe(yearly_expenses_df)

            with col2:
                if chart_type in CHART_TYPES:
                    filtered_chart_df = filtered_df[filtered_df['amount_paid'] > 0]
                    dv.display_yearly_expenses(filtered_chart_df, selected_year, chart_type)
                else:
                    st.warning(f"Invalid chart type selected: {chart_type}")

            insights = get_insights(filtered_df)



    # Data Insights display
    if insights:
        ExpenseSummaryInsights(insights).display()

    # Subcategory Visualization
    if detailed_view_category:
        st.markdown("---")
       # st.markdown("<h3 style='text-align: center;'>🧾 Subcategory Expenses Details</h3>", unsafe_allow_html=True)
        heading = Heading("📂 Subcategory Expense Breakdown")
        heading.display_centered()

        subcategory_df = dv.get_user_expenses_by_subcategory(
            cleaned_df,
            selected_year=selected_year,
            selected_month=selected_month,
            category=detailed_view_category
        )

        if subcategory_df.empty:
            st.warning(f"No data available for subcategory expenses under '{detailed_view_category}'.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"##### 💰 Top 10 Subcategory Expenses for Category - {detailed_view_category}")
                top_subcategories_df = (
                    subcategory_df.groupby('subcategory_name', as_index=False)
                    .agg(total_amount=('total_amount', 'sum'))
                )
                top_subcategories_df = top_subcategories_df[top_subcategories_df['total_amount'] > 0]
                top_subcategories_df = top_subcategories_df.sort_values(by='total_amount', ascending=False).head(10)
                st.dataframe(top_subcategories_df)

            with col2:
                st.markdown("""
                        <div style="text-align: center;">
                            <h5>📊 Horizontal Bar Chart: Subcategory Expenses</h5>
                        </div>
                    """, unsafe_allow_html=True)

                filtered_subcategory_df = subcategory_df[subcategory_df['total_amount'] > 0]
                dv.display_subcategory_expenses(
                    filtered_subcategory_df,
                    selected_year=selected_year,
                    selected_month=selected_month,
                    category=detailed_view_category
                )

            st.markdown("---")

            heading = Heading(f"💳 Payment Modes Overview")
            heading.display_centered()
            col3, col4 = st.columns(2)

            with col3:
                
                st.markdown(f"##### 📊 Payment Modes Category for category-{detailed_view_category}")

                payment_mode_count_df = dv.get_payment_mode_count(
                    payment_mode_df,
                    selected_year=selected_year,
                    selected_month=selected_month,
                    category=detailed_view_category
                )
                if payment_mode_count_df.empty:
                    st.warning("No data available for payment modes.")
                else:
                    st.dataframe(payment_mode_count_df)
               
                payment_modes_insights = get_payment_mode_insights(payment_mode_count_df)

                # Data Insights display
                if payment_modes_insights:
                    PaymentModesInsights(payment_modes_insights).display()    

            with col4:
                st.markdown("""
                    <div style="text-align: center;">
                        <h5>📊 Top 10 Payment Methods for Transactions</h5>
                    </div>
                """, unsafe_allow_html=True)


                if not payment_mode_count_df.empty:
                    # Ensure 'count' column is numeric
                    payment_mode_count_df['count'] = pd.to_numeric(payment_mode_count_df['count'], errors='coerce')
                    
                    # Remove rows with NaN in 'count'
                    payment_mode_count_df = payment_mode_count_df.dropna(subset=['count'])
                    
                    if payment_mode_count_df.empty:
                        st.warning("No valid numeric data available for payment modes.")
                    else:
                        # Limit to Top 10 payment modes by Count
                        payment_mode_count_df = payment_mode_count_df.sort_values(by='count', ascending=False).head(10)
                        
                        # Plot the bar chart directly
                        plot_bar_chart_payment(
                            payment_mode_count_df.set_index('payment_mode_name')['count'],
                            "Payment Modes",
                            "Count",
                            "Top 10 Payment Modes Chart"
                        )


   
                     


if __name__ == "__main__":
    main()
