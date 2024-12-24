import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

def save_chart_as_image(chart, filename):
    """Save chart as an image file."""
    chart_path = f"/tmp/{filename}.png"
    chart.savefig(chart_path, format="png")
    return chart_path

def save_as_pdf(df, chart, filename="expenses_report.pdf"):
    """Generate and save PDF with both the chart and the table."""
    pdf_path = f"/tmp/{filename}"
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Draw Table
    data = [df.columns.tolist()] + df.values.tolist()
    table_width = width - 100
    table_height = height - 300
    x_offset = 50
    y_offset = table_height

    for row in data:
        pdf.drawString(x_offset, y_offset, "   ".join(str(item) for item in row))
        y_offset -= 15
    
    # Draw Chart
    chart_path = save_chart_as_image(chart, "chart")
    pdf.drawImage(chart_path, 50, y_offset - 200, width=500, height=200)

    pdf.save()
    return pdf_path

def save_as_csv(df):
    """Save DataFrame to CSV."""
    path = f"/tmp/expenses.csv"
    df.to_csv(path, index=False)
    return path

def capture_screenshot(filename="screenshot.png"):
    """Capture a screenshot and save it."""
    screenshot_path = f"/tmp/{filename}"
    st.screenshot(screenshot_path)
    return screenshot_path
