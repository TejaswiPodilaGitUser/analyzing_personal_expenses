import matplotlib.pyplot as plt

def plot_scatter_chart(df, x, y, title, chart_size=(6, 4), label_rotation=45):
    """Plot a scatter chart with label rotation."""
    fig, ax = plt.subplots(figsize=chart_size)
    
    ax.scatter(df[x], df[y], c='blue', edgecolors='black', alpha=0.7)
    ax.set_xlabel(x, fontsize=12, fontweight='bold')
    ax.set_ylabel(y, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Rotate X-axis labels for better readability
    plt.xticks(rotation=label_rotation, ha='right', fontsize=10)  # label_rotation can be adjusted as needed

    # Optional: Add grid for better visualization
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Display the plot
    plt.tight_layout()
    return fig
