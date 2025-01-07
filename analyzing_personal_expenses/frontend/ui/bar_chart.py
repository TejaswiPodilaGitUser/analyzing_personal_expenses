import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

import matplotlib.cm as cm
import matplotlib.colors as mcolors



def plot_bar_chart(data, xlabel, ylabel, title, chart_size=(6, 4)):
    """Plot a bar chart with consistent bar width for wide layouts and fewer bars."""
    
    fig, ax = plt.subplots(figsize=chart_size)
    
    # Sort data by values for consistent ordering
    data = data.sort_values(ascending=False)
    
    # Normalize the data values to map to the colormap
    norm = plt.Normalize(data.values.min(), data.values.max())
    colors = plt.cm.coolwarm(norm(data.values))  # Using the 'coolwarm' colormap
    
    # Handle bar width dynamically
    if len(data) < 4:
        bar_width = 0.2  # Narrower bars for 1-3 bars
    else:
        bar_width = 0.6  # Standard width for larger datasets
    
    # Adjust positions for few bars to avoid stretching
    x_positions = np.arange(len(data))
    bars = ax.bar(x_positions, data.values, color=colors, width=bar_width, align='center')
    
    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, 
                yval + 0.01 * yval, 
                f'{yval:,.2f}', 
                ha='center', va='bottom', fontsize=8, rotation=20)
    
    # Set labels and title
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    #ax.set_title(title, fontweight='bold')
    
    # Improve x-axis readability
    ax.set_xticks(x_positions)
    ax.set_xticklabels(data.index, rotation=30, ha='right', fontsize=10)
    
    # Adjust axis limits to prevent bars from stretching excessively
    if len(data) < 4:
        ax.set_xlim(-0.5, len(data) - 0.5)  # Tighten x-axis range for fewer bars
    
    # Improve layout
    plt.tight_layout()
    st.pyplot(fig)




def plot_bar_chart_payment(data, xlabel, ylabel, title, chart_size=(8, 6)):
    """Plot a bar chart with dynamic colors and consistent bar width for various data sizes."""
    
    fig, ax = plt.subplots(figsize=chart_size)
    
    # Sort data by values for consistent ordering
    data = data.sort_values(ascending=False)
    
    # Normalize data values for color mapping
    norm = mcolors.Normalize(vmin=data.values.min(), vmax=data.values.max())
    colors = cm.viridis(norm(data.values))  # 'viridis' for better visual contrast
    
    # Handle bar width dynamically based on data size
    if len(data) < 4:
        bar_width = 0.3  # Narrower bars for 1-3 bars
    else:
        bar_width = 0.6  # Standard width for larger datasets
    
    # Adjust positions for the bars
    x_positions = np.arange(len(data))
    bars = ax.bar(x_positions, data.values, color=colors, width=bar_width, edgecolor='black')
    
    # Add value labels on top of bars (No Decimals)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, 
                yval + (0.05 * yval if yval > 0 else 0.02), 
                f'{int(yval)}',  # Display as integer
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')
    
    # Set labels and title
    ax.set_xlabel(xlabel, fontweight='bold', fontsize=11)
    ax.set_ylabel(ylabel, fontweight='bold', fontsize=11)
    #ax.set_title(title, fontweight='bold', fontsize=13, pad=15)
    
    # Improve x-axis readability
    ax.set_xticks(x_positions)
    ax.set_xticklabels(data.index, rotation=30, ha='right', fontsize=10)
    
    # Adjust axis limits for small datasets
    if len(data) < 4:
        ax.set_xlim(-0.5, len(data) - 0.5)
    
 
    # Improve layout
    plt.tight_layout()
    st.pyplot(fig)