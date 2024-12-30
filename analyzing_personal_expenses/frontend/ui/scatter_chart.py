import matplotlib.pyplot as plt
import streamlit as st

def plot_scatter_chart(data, title, chart_size=(6, 4)):
    """Plot a scatter plot for expense outliers."""
    fig, ax = plt.subplots(figsize=chart_size)
    
    # Plot scatter points
    ax.scatter(data.index, data.values, color='b', alpha=0.5)
    
    ax.set_xlabel('Categories', fontweight='bold')
    ax.set_ylabel('Amount Paid', fontweight='bold')
    #ax.set_title(title, fontweight='bold')
    
    # Rotate x-axis labels for better readability
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=45, ha='right', fontsize=8)
    
    # Adjust aspect ratio automatically
    ax.set_aspect('auto')  # Ensures no forced aspect ratio
    
    plt.tight_layout()
    st.pyplot(fig)
