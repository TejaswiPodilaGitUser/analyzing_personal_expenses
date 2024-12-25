import pandas as pd
import matplotlib.pyplot as plt


def plot_bar_chart(data, xlabel, ylabel, title):
    """Plot a bar chart."""
    data.plot(kind='bar')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def plot_pie_chart(data, title):
    """Plot a pie chart."""
    data.plot(kind='pie', autopct='%1.1f%%')
    plt.title(title)
    plt.show()


def save_as_csv(df, user_name, selected_month):
    """Save data to CSV."""
    filename = f"{user_name}_{selected_month}_top_10_expenses.csv"
    df.to_csv(filename)
    return filename


def save_as_pdf(df):
    """Save data to PDF."""
    filename = "top_10_expenses.pdf"
    # PDF saving logic goes here
    return filename


def capture_screenshot(filename):
    """Capture screenshot."""
    # Screenshot capturing logic goes here
    return filename
