import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_bar_chart(data, xlabel, ylabel, title, chart_size=(8, 6)):
    """Plot a bar chart with consistent sizing, proper label alignment, and spacing."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for better label spacing
    
    # Sort data by values for consistent ordering (optional)
    data = data.sort_values(ascending=False)
    
    # Normalize the data values to map to the colormap
    norm = plt.Normalize(data.values.min(), data.values.max())
    colors = plt.cm.coolwarm(norm(data.values))  # Using the 'coolwarm' colormap
    
    # Plot the bar chart with color mapping
    bars = ax.bar(data.index, data.values, color=colors)
    
    # Add value labels on top of bars (optional)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, 
                yval + 0.01 * yval,  # Position the text slightly above the bar
                f'{yval:,.2f}', 
                ha='center', va='bottom', fontsize=8, rotation=20)  # Rotating the text by 45 degrees
    
    # Set labels and title
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold')
    
    # Improve label readability with rotated x-axis labels
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=60, ha='right', fontsize=10)
    

    # Add padding around the plot to avoid text touching the borders
    plt.subplots_adjust(left=0.01, right=0.02, top=3.5, bottom=0.1)  # Adjust these values to control padding
   

    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Add more space for the x-axis labels
    st.pyplot(fig)
