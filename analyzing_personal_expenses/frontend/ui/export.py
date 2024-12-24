import streamlit as st
from frontend.ui.export_data import save_as_csv, save_as_pdf, capture_screenshot

def handle_export(df):
    # Centered Data Insights Section
    st.markdown("---")  # Add a visual separator
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <h3>📊 Expense Summary: Key Spending Insights</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    insights = df.get_insights(df)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p><strong>▲ Max Spending:</strong> {insights['max_category']} (${insights['max_amount']:.2f})</p>
            <p><strong>▼ Min Spending:</strong> {insights['min_category']} (${insights['min_amount']:.2f})</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Export options only after visualization
    st.sidebar.title("Export Data")
    export_option = st.sidebar.selectbox("Select Export Option", ["CSV", "PDF", "Screenshot"], index=0)
    
    if export_option == "CSV":
        # Export only the top 10 data displayed
        filename = save_as_csv(df)
        st.sidebar.download_button("Download CSV", open(filename, "rb").read(), filename)
    elif export_option == "PDF":
        # Export only the top 10 data displayed
        filename = save_as_pdf(df)
        st.sidebar.download_button("Download PDF", open(filename, "rb").read(), filename)
    elif export_option == "Screenshot":
        # Capture the screenshot
        screenshot_path = capture_screenshot(filename="streamlit_screenshot.png")
        st.sidebar.download_button(
            label="Download Screenshot",
            data=open(screenshot_path, "rb").read(),
            file_name="streamlit_screenshot.png",
            mime="image/png"
        )
