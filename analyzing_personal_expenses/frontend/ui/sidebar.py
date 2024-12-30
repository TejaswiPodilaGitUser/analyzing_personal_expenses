import streamlit as st
from utils.static_expense_data import MONTHS, YEARS
from backend.database.db_operations import DatabaseOperations
from typing import Dict, Tuple, Optional

def display_sidebar(users: Dict[str, int]) -> Tuple[Optional[int], str, str, Optional[str], Optional[str], Optional[str]]:
    """
    Display the sidebar with user filters and return selected values.
    Ensures a tuple is always returned with the expected values.
    """
    st.sidebar.title("Choose Filters")

    # Select user
    user_id = select_user(users)
    
    # Select visualization type (Yearly or Monthly)
    visualization_type = select_visualization_type()

    # Select year
    selected_year = select_year()
    if not selected_year:
        selected_year = YEARS[0] if YEARS else "2025"  # Ensure fallback year is valid

    # Select month if Monthly visualization is chosen
    selected_month = None
    if visualization_type == "Monthly":
        selected_month = select_month()

    # Select chart type (Pie, Bar, etc.)
    chart_type = select_chart_type()

    # Select category for detailed view (if detailed view is enabled)
    detailed_view_category = select_category(user_id)

    return user_id, visualization_type, chart_type, selected_month, selected_year, detailed_view_category


def select_user(users: Dict[str, int]) -> Optional[int]:
    """
    Display user selection dropdown in the sidebar.
    """
    user_name = st.sidebar.selectbox("Select User", ["All Users"] + list(users.keys()), index=0)
    return None if user_name == "All Users" else users[user_name]


def select_visualization_type() -> str:
    """
    Display visualization type radio buttons in the sidebar.
    """
    return st.sidebar.radio("Analysis Period", ["Yearly", "Monthly"], index=0)


def select_year() -> Optional[str]:
    """
    Display year selection dropdown in the sidebar.
    """
    if YEARS:
        return st.sidebar.selectbox("Select Year", YEARS, index=0)
    else:
        st.sidebar.warning("No years available in the database.")
        return None


def select_month() -> Optional[str]:
    """
    Display month selection dropdown in the sidebar.
    """
    return st.sidebar.selectbox("Select Month", MONTHS, index=0)


def select_chart_type() -> str:
    """
    Display chart type dropdown in the sidebar.
    """
    return st.sidebar.selectbox("Chart Type", ["Pie", "Bar", "Scatter", "Line"], index=0)


# For the selected user_id, Selected year and Month
# Display the category selection dropdown in the sidebar
# Only after clicking 'More Detailed View'
# Return the selected category
def select_category(user_id: Optional[int]) -> Optional[str]:
    """
    Display category selection dropdown in the sidebar only after clicking 'More Detailed View'.
    """
    if 'show_detailed_view' not in st.session_state:
        st.session_state['show_detailed_view'] = False

    if st.sidebar.button("More Detailed View"):
        st.session_state['show_detailed_view'] = not st.session_state['show_detailed_view']

    if st.session_state['show_detailed_view']:
        db_ops = DatabaseOperations()
        try:
            print("Fetching categories...user_id:", user_id)
            #Add All Categories to the list of categories
            categories = db_ops.fetch_user_categories(user_id) if user_id is not None else db_ops.fetch_all_categories()
            categories.insert(0, "All Categories")
            if not categories:
                st.sidebar.warning("No categories available.")
                return None
            category_name = st.sidebar.selectbox("Select Category", categories)
            st.session_state['detailed_view_category'] = category_name
            return category_name
        except Exception as e:
            st.sidebar.error(f"Error fetching categories: {e}")
            return None