import matplotlib.pyplot as plt
import streamlit as st


def plot_pie_chart(data, title, chart_size=(6, 4)):
    """Plot a pie chart with proper sizing and title."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for consistency
    
    data.plot(
        kind='pie',
        autopct='%1.1f%%',
        ax=ax,
        legend=False,
        startangle=140
    )
    
    ax.set_ylabel('')  # Remove the y-axis label for a cleaner look
   # ax.set_title(title, fontweight='bold')  # Add title with bold formatting
    
    plt.tight_layout()
    st.pyplot(fig)
