import streamlit as st

class GeneralStyling:
    @staticmethod
    def apply_styling():
        # Custom CSS for styling the app
        st.markdown("""
        <style>
            /* General Title Styling */
            .section-title {
                font-size: 24px;
                font-weight: bold;
                color: #2F4F4F;
                margin-top: 20px;
                margin-bottom: 20px;
            }

            /* Insights Text */
            .insight-text {
                font-size: 18px;
                color: #4B0082;
                margin-top: 10px;
            }

            /* Sidebar Title Styling */
            .sidebar-title {
                font-size: 22px;
                font-weight: bold;
                color: #2F4F4F;
            }

            /* Sidebar dropdowns */
            .streamlit-expanderHeader {
                font-size: 18px;
                color: #4B0082;
            }

            /* Dataframe Styling */
            .stDataFrame {
                border: 2px solid #4B0082;
                border-radius: 8px;
                padding: 10px;
            }

            /* Large Chart Size */
            .chart-container {
                width: 100%;
                height: 600px;
                margin-bottom: 20px;
            }

            /* Larger Plot Titles */
            .plot-title {
                font-size: 20px;
                font-weight: bold;
                color: #2F4F4F;
            }
        </style>
        """, unsafe_allow_html=True)

