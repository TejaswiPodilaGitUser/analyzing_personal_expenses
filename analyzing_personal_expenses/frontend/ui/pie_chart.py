import matplotlib.pyplot as plt
import streamlit as st

def plot_pie_chart(data, title, chart_size=(8, 8)):
    fig, ax = plt.subplots()
    data.plot(kind='pie', autopct='%1.1f%%', ax=ax, legend=False, startangle=140)
    ax.set_ylabel('')  # Remove the y-axis label
   # ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)
