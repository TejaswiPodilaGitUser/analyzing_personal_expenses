import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_bar_chart(data, xlabel, ylabel, title, chart_size=(6, 4)):
    """Plot a bar chart with consistent sizing and color mapping."""
    fig, ax = plt.subplots(figsize=chart_size)  # Explicit figsize for consistency
    
    # Normalize the data values to map to the colormap
    norm = plt.Normalize(data.values.min(), data.values.max())
    colors = plt.cm.coolwarm(norm(data.values))  # Using the 'coolwarm' colormap
    
    # Plot the bar chart with color mapping
    bars = ax.bar(data.index, data.values, color=colors)
    
    # Set labels and title
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    #ax.set_title(title, fontweight='bold')  # Set title
    
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    st.pyplot(fig)