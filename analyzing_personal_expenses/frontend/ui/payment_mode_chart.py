import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


class PaymentModeChart:
    """
    Class to display Payment Mode Bar Chart with enhanced customization.
    """

    def __init__(self, payment_mode_df: pd.DataFrame):
        """
        Initialize with payment mode DataFrame.
        
        Args:
            payment_mode_df (pd.DataFrame): DataFrame containing payment mode data.
        """
        self.payment_mode_df = payment_mode_df

    def display_chart(self):
        """
        Display the Payment Mode Bar Chart in Streamlit.
        """
        if self.payment_mode_df.empty:
            st.warning("No payment mode data available to display.")
            return

        # Prepare DataFrame for plotting
        payment_mode_chart = self.payment_mode_df.set_index('payment_mode_name')

        # Plot with Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3))  # Customize size if needed

        bars = ax.bar(
            payment_mode_chart.index,
            payment_mode_chart['count'],
            color='skyblue',
            edgecolor='black'
        )

        # Add labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                f"{int(yval)}",  # Display count value
                ha='center',
                va='bottom',
                fontsize=8
            )

        # Rotate x-axis labels for clarity
        ax.set_xticklabels(payment_mode_chart.index, rotation=45, ha='right', fontsize=8)

        # Titles and labels
        ax.set_title('Payment Mode Distribution', fontsize=12, fontweight='bold')
        ax.set_xlabel('Payment Modes', fontsize=10, fontweight='bold')
        ax.set_ylabel('Count', fontsize=10, fontweight='bold')

        # Adjust spacing
        plt.tight_layout()

        # Display the chart in Streamlit
        st.pyplot(fig)
