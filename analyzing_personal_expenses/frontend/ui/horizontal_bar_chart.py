import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plot_horizontal_bar_chart(data: pd.DataFrame, category_name: str):
    """
    Plot a horizontal bar chart for subcategory expenses.

    Args:
        data (pd.DataFrame): DataFrame containing subcategory expenses.
        category_name (str): Name of the category for the title.
    """
    # Ensure there are data to plot
    if data.empty:
        st.warning(f"No data available for the subcategory: {category_name}")
        return

    # Set a smaller figure size
    plt.figure(figsize=(5, 3))  # You can adjust this for a smaller or larger plot

    # Plot the data
    data.set_index('subcategory_name')['total_amount'].plot(kind='barh', color='skyblue')

    # Add labels to bars with smaller font size
    for index, value in enumerate(data['total_amount']):
        plt.text(value, index, f"${value:.2f}", va='center', fontsize=8)  # Smaller font for text

    # Title and labels with smaller font sizes
    plt.title(f"Top Subcategory Breakdown - {category_name}", fontsize=10)  # Smaller title font
    plt.xlabel('Total Amount', fontsize=8)  # Smaller xlabel font
    plt.ylabel('Subcategory', fontsize=8)  # Smaller ylabel font
    
    # Adjust the layout and make it tight
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)
