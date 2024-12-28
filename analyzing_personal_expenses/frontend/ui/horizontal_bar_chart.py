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
    plt.figure(figsize=(10, 6))
    data.set_index('subcategory_name')['total_amount'].plot(kind='barh', color='skyblue')
    #Show total amount on the bars
    for index, value in enumerate(data['total_amount']):
        plt.text(value, index, f"${value:.2f}")
    plt.title(f"Subcategory Breakdown - {category_name}")
    plt.xlabel('Total Amount')
    plt.ylabel('Subcategory')
    plt.tight_layout()
    st.pyplot(plt)