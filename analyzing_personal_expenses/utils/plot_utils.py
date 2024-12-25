import pandas as pd
import os
from fpdf import FPDF

def save_as_csv(df, user_name, selected_month):
    """Save data to CSV with appropriate naming."""
    # Handle different cases for filename generation
    if selected_month is None:
        if user_name == "All Users":
            filename = "All_Users_Annual_Top_10_Expenses.csv"
        else:
            filename = f"{user_name}_Annual_Top_10_Expenses.csv"
    else:
        if user_name == "All Users":
            filename = f"All_Users_{selected_month}_Top_10_Expenses.csv"
        else:
            filename = f"{user_name}_{selected_month}_Top_10_Expenses.csv"
    
    # Save the DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"CSV file saved as: {filename}")
    return filename


def save_as_pdf(df, user_name, selected_month=None):
    """Save data to PDF with a dynamic filename based on user and month selection."""
    try:
        # Handle dynamic filename generation based on user and selected month
        if selected_month is None:
            if user_name == "All Users":
                filename = "All_Users_Annual_Top_10_Expenses.pdf"
            else:
                filename = f"{user_name}_Annual_Top_10_Expenses.pdf"
        else:
            if user_name == "All Users":
                filename = f"All_Users_{selected_month}_Top_10_Expenses.pdf"
            else:
                filename = f"{user_name}_{selected_month}_Top_10_Expenses.pdf"
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Top 10 Expenses", ln=True, align='C')

        # Add headers
        headers = df.columns
        for header in headers:
            pdf.cell(40, 10, txt=str(header), border=1)
        pdf.ln()

        # Add rows of data
        for _, row in df.iterrows():
            for item in row:
                pdf.cell(40, 10, txt=str(item), border=1)
            pdf.ln()

        # Output PDF with the dynamically generated filename
        pdf.output(filename)
        print(f"PDF file saved as: {filename}")
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
