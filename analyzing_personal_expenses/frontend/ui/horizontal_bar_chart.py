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
    
    # Adjust bar width based on the number of subcategories
    if num_subcategories == 1:
        bar_width = 0.1  # Very thin bar for a single subcategory
    elif num_subcategories < 4:
        bar_width = 0.3  # Thin bars for a few subcategories
    else:
        bar_width = 0.5  # Wider bars for many subcategories

    # Set the figure size
    plt.figure(figsize=(6, 4))

    # Plot the data with default colors and adjusted bar width
    data.set_index('subcategory_name')['total_amount'].plot(
        kind='barh', 
        width=bar_width
    )

    # Add labels to bars with smaller font size
    for index, value in enumerate(data['total_amount']):
        plt.text(value, index, f"${value:.2f}", va='center', fontsize=8)

    # Title and labels with smaller font sizes
    #plt.title(f"Top Subcategory Breakdown - {category_name}", fontsize=12, fontweight='bold')
    plt.xlabel('Total Amount', fontsize=10, fontweight='bold')
    plt.ylabel('Subcategory', fontsize=10, fontweight='bold')

    # Adjust the layout and make it tight
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)
