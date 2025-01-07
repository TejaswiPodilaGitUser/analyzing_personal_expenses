import matplotlib.pyplot as plt
import streamlit as st

def plot_pie_chart(data, title, labels, chart_size=(6, 4), label_fontsize=10, label_rotation=10, percentage_rotation=35):
    """Plot a pie chart with proper sizing, avoid overlapping labels, and allow rotation of labels and percentages."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for consistency

    # Plot the pie chart with adjusted distances
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,  # Category names as labels
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': label_fontsize},
        pctdistance=0.85,  # Move percentage labels slightly inward
        labeldistance=1.1  # Move category labels slightly outward
    )
    
    # Rotate labels and percentages
    for text in texts:
        text.set_rotation(label_rotation)  # Rotate label texts
    
    for autotext in autotexts:
        autotext.set_rotation(percentage_rotation)  # Rotate percentage texts
    
    # Remove y-axis label for a cleaner look
    ax.set_ylabel('')  
    
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')  
    
    # Set title
    #ax.set_title(title, fontsize=12)

    plt.tight_layout()
    st.pyplot(fig)
