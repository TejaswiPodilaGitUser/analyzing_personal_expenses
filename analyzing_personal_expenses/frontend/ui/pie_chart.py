import matplotlib.pyplot as plt
import streamlit as st


def plot_pie_chart(data, title, chart_size=(6, 4)):
    """Plot a pie chart with proper sizing and title."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for consistency

    # Plot the pie chart
    wedges, texts, autotexts = ax.pie(
        data,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 8}
    )
    
    ax.set_ylabel('')  # Remove the y-axis label for a cleaner look
    ax.set_title(title, fontweight='bold', fontsize=10)
    
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')  
    
    plt.tight_layout()
    st.pyplot(fig)
