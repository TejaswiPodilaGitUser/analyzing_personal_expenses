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
    # Ensure there is data to plot
    if data.empty:
        st.warning(f"No data available for the subcategory: {category_name}")
        return

    # Calculate the number of subcategories
    num_subcategories = len(data)
    
    # Adjust the width of bars based on the number of subcategories
    bar_width = 0.2 if num_subcategories < 4 else 0.5  # Decrease bar width for larger number of bars

    # Set the figure size
    plt.figure(figsize=(8, 5))

    # Plot the data with adjusted bar width
    data.set_index('subcategory_name')['total_amount'].plot(kind='barh', color='skyblue', width=bar_width)

    # Add labels to bars with smaller font size
    for index, value in enumerate(data['total_amount']):
        plt.text(value, index, f"${value:.2f}", va='center')  # Smaller font for text

    # Title and labels with smaller font sizes
   # plt.title(f"Top Subcategory Breakdown - {category_name}", fontsize=10)  # Smaller title font
    plt.xlabel('Total Amount', fontweight='bold')  # Smaller xlabel font
    plt.ylabel('Subcategory', fontweight='bold')  # Smaller ylabel font

    # Adjust the layout and make it tight
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)
