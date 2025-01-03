import streamlit as st
from utils.static_expense_data import MONTHS, YEARS, CHARTTYPE
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
        selected_year = YEARS[0] if YEARS else "2024"  # Ensure fallback year is valid

    # Select month if Monthly visualization is chosen
    selected_month = None
    if visualization_type == "Monthly":
        selected_month = select_month()

    # Select chart type (Pie, Bar, etc.)
    chart_type = select_chart_type()

    # Select category for detailed view (if detailed view is enabled)
    detailed_view_category = select_category(user_id, selected_year, selected_month)

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
    Display year selection dropdown in the sidebar with 2024 as the default year.
    """
    if YEARS:
        default_year = "2024"
        index = YEARS.index(default_year) if default_year in YEARS else 0
        return st.sidebar.selectbox("Select Year", YEARS, index=index)
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
    Display chart type dropdown in the sidebar with 'Pie' as the default.
    """
    chart_types = list(CHARTTYPE)  # Convert set to list
    default_index = chart_types.index("Pie") if "Pie" in chart_types else 0
    return st.sidebar.selectbox("Chart Type", chart_types, index=default_index)



def select_category(user_id: Optional[int], selected_year: Optional[str], selected_month: Optional[str]) -> Optional[str]:
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
            # Fetch categories based on user_id, year, and month if applicable
            categories_df = db_ops.fetch_user_categories(user_id, selected_year, selected_month)

            # Debug: Show columns to verify structure
           # st.sidebar.write("Category DataFrame Columns:", categories_df.columns.tolist())

            if not categories_df.empty and 'category_name' in categories_df.columns:
                categories = ["All Categories"] + categories_df['category_name'].tolist()
            else:
                #st.sidebar.warning("No valid categories found. Fetching all categories as fallback.")
                categories_df = db_ops.fetch_all_categories()
                if not categories_df.empty and 'category_name' in categories_df.columns:
                    categories = ["All Categories"] + categories_df['category_name'].tolist()
                else:
                    categories = ["All Categories"]
            
            # Select category from the dropdown
            category_name = st.sidebar.selectbox("Select Category", categories)
            st.session_state['detailed_view_category'] = category_name
            return category_name

        except Exception as e:
            st.sidebar.warning("No valid categories found")
            return None

    return None
