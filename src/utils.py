import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def setup_plotting_style():
    """Sets up a nice plotting style."""
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (12, 6)

def plot_miner_distribution(df, title="Miner Block Production Distribution"):
    """Plots the number of blocks mined by each address."""
    miner_counts = df['miner'].value_counts()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=miner_counts.index, y=miner_counts.values, palette="viridis")
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel("Miner Address")
    plt.ylabel("Blocks Mined")
    plt.tight_layout()
    plt.show()

def plot_block_times(df):
    """Plots the time difference between blocks."""
    df['time_diff'] = df['timestamp'].diff()
    plt.figure(figsize=(12, 4))
    sns.lineplot(data=df, x='block_number', y='time_diff')
    plt.title("Block Production Time Intervals")
    plt.xlabel("Block Number")
    plt.ylabel("Time Since Last Block (s)")
    plt.show()
