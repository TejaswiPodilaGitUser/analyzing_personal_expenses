import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_bar_chart(data, xlabel, ylabel, title, chart_size=(10, 6)):
    fig, ax = plt.subplots(figsize=chart_size)
    
    # Normalize the data values to map to the colormap
    norm = plt.Normalize(data.values.min(), data.values.max())
    colors = plt.cm.coolwarm(norm(data.values))  # Use the 'viridis' colormap
    
    # Plot the bar chart with the colormap
    bars = ax.bar(data.index, data.values, color=colors)
    
    # Set labels and title
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
   # ax.set_title(title, fontweight='bold')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)