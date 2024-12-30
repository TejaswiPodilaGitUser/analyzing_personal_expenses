import matplotlib.pyplot as plt
import streamlit as st


def plot_pie_chart(data, title, labels, chart_size=(6, 4),label_fontsize=12):
    """Plot a pie chart with proper sizing and title."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for consistency

    # Plot the pie chart
    wedges, texts, autotexts = ax.pie(
            data,
            labels=labels,  # Category names as labels
            autopct='%1.1f%%',
            startangle=140,
            textprops={'fontsize': label_fontsize}
        )
    
    # add code to set label
    ax.set_ylabel('')  # Remove the y-axis label for a cleaner look
    #ax.set_title(title, fontweight='bold', fontsize=10)
    
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')  
    
    plt.tight_layout()
    st.pyplot(fig)
