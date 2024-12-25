import pandas as pd
import os
from fpdf import FPDF

def save_as_csv(df, user_name, selected_month):
    """Save data to CSV."""
    # Debugging statement
    print(f"In Plot_utils . Saving data to CSV for user: {user_name} and month: {selected_month}")
    
    # Handle different cases for filename generation
    if user_name == "All Users" and selected_month is None:
        filename = "All_Users_top_10_Annual_expenses.csv"
    else:
        filename = f"{user_name}_{selected_month}_top_10_expenses.csv"
    
    df.to_csv(filename, index=False)
    return filename



def save_as_pdf(df):
    """Save data to PDF."""
    filename = "top_10_expenses.pdf"
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Top 10 Expenses", ln=True, align='C')

        headers = df.columns
        for header in headers:
            pdf.cell(40, 10, txt=str(header), border=1)
        pdf.ln()

        for _, row in df.iterrows():
            for item in row:
                pdf.cell(40, 10, txt=str(item), border=1)
            pdf.ln()

        pdf.output(filename)
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
