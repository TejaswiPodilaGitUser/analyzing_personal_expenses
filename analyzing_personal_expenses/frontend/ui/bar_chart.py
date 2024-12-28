import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_bar_chart(data, xlabel, ylabel, title, chart_size=(6, 4)):
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
        ax.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height(), 
                f'{bar.get_height():,.2f}', 
                ha='center', va='bottom', fontsize=8)
    
    # Set labels and title
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    #ax.set_title(title, fontweight='bold')
    
    # Improve label readability
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=45, ha='right', fontsize=8)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    st.pyplot(fig)
