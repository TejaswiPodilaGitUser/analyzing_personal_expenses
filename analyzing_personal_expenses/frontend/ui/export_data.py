import pandas as pd
import streamlit as st
from utils.plot_utils import save_as_csv, save_as_pdf, capture_screenshot


class ExportData:
    def __init__(self, df, selected_month, user_name):
        self.df = df
        self.selected_month = selected_month
        self.user_name = user_name

    def display(self):
        """Handles export options for CSV, PDF, and Screenshot"""
        export_option = st.sidebar.selectbox("Select Export Option", ["CSV", "PDF", "Screenshot"], index=0)

        if self.df is not None and not self.df.empty:
            if export_option == "CSV":
                self._export_csv()
            elif export_option == "PDF":
                self._export_pdf()
            elif export_option == "Screenshot":
                self._export_screenshot()
        else:
            st.warning("No data available for export.")

    def _export_csv(self):
        """Handles the CSV export."""
        filename = save_as_csv(self.df, self.user_name, self.selected_month)
        st.sidebar.download_button("Download CSV", open(filename, "rb").read(), filename)

    def _export_pdf(self):
        """Handles the PDF export."""
        filename = save_as_pdf(self.df)
        st.sidebar.download_button("Download PDF", open(filename, "rb").read(), filename)

    def _export_screenshot(self):
        """Handles the screenshot export."""
        screenshot_path = capture_screenshot(filename="streamlit_screenshot.png")
        st.sidebar.download_button(
            label="Download Screenshot",
            data=open(screenshot_path, "rb").read(),
            file_name="streamlit_screenshot.png"
        )
