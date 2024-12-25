import pandas as pd
import streamlit as st
from utils.plot_utils import save_as_csv, save_as_pdf
import os
class ExportData:
    def __init__(self, df, selected_month, user_name):
        self.df = df
        self.selected_month = selected_month
        self.user_name = user_name

    def display(self):
        """Handles export options for CSV and PDF."""
        export_option = st.sidebar.selectbox("Select Export Option", ["CSV", "PDF"], index=0)

        if self.df is not None and not self.df.empty:
            if export_option == "CSV":
                self.export_csv()
            elif export_option == "PDF":
                self.export_pdf()
        else:
            st.warning("No data available for export.")

    def export_csv(self):
        """Handles CSV export."""
        try:
            filename = save_as_csv(self.df, self.user_name, self.selected_month)
            with open(filename, "rb") as file:
                st.sidebar.download_button("Download CSV", file.read(), file_name=filename)
        except Exception as e:
            st.error(f"Failed to export CSV: {e}")
