import matplotlib.pyplot as plt
import streamlit as st

def plot_line_chart(data, xlabel, ylabel, title, chart_size=(6, 4)):
    """Plot a line chart for expense trends."""
    fig, ax = plt.subplots(figsize=chart_size)
    data.plot(kind='line', marker='o', ax=ax)
    
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
   # ax.set_title(title, fontweight='bold')

    # Rotate x-axis labels for better readability
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=45, ha='right', fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
