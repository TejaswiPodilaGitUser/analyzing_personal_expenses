import streamlit as st

class Heading:
    def __init__(self, text):
        self.text = text

    def display_centered(self):
        """Displays the heading text centered."""
        st.markdown(f"<h3 style='text-align: center;'>{self.text}</h3>", unsafe_allow_html=True)
