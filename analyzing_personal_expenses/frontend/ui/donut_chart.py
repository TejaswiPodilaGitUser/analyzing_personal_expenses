import matplotlib.pyplot as plt
import streamlit as st

def plot_donut_chart(data, title, labels, chart_size=(6, 4), label_fontsize=12, hole_radius=0.5):
    """Plot a donut chart with proper sizing and title."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for consistency

    # Plot the donut chart
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,  # Category names as labels
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': label_fontsize},
        wedgeprops={'width': hole_radius}  # Create the hole in the center
    )
    
    # Add the title
   # ax.set_title(title, fontweight='bold', fontsize=14)

    # Remove the y-axis label for a cleaner look
    ax.set_ylabel('')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')  
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    # Show the plot in Streamlit
    st.pyplot(fig)
