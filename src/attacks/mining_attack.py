import pandas as pd
import numpy as np

def calculate_miner_metrics(df):
    """
    Calculates the percentage of blocks mined by each miner.
    Returns a DataFrame with miner stats.
    """
    total_blocks = len(df)
    miner_counts = df['miner'].value_counts()
    miner_share = miner_counts / total_blocks
    
    stats = pd.DataFrame({
        'blocks_mined': miner_counts,
        'share': miner_share
    })
    return stats

def detect_51_percent_attack(miner_stats, threshold=0.50):
    """
    Checks if any miner controls more than the threshold share (default 50%).
    Returns a list of suspicious miners.
    """
    suspicious = miner_stats[miner_stats['share'] > threshold]
    if not suspicious.empty:
        print(f"ALERT: Potential 51% Attack Detected! Miners above {threshold*100}%:")
        print(suspicious)
        return suspicious.index.tolist()
    else:
        print("No single miner controls > 50% of the network.")
        return []

def calculate_gini_coefficient(miner_stats):
    """
    Calculates the Gini coefficient of mining centralization.
    0 = perfect equality, 1 = perfect inequality.
    """
    shares = miner_stats['share'].values
    shares = np.sort(shares)
    n = len(shares)
    index = np.arange(1, n + 1)
    return ((np.sum((2 * index - n  - 1) * shares)) / (n * np.sum(shares)))

def detect_timestamp_manipulation(df, z_threshold=3):
    """
    Detects anomalies in block timestamps using Z-score.
    Miners might manipulate timestamps for difficulty adjustment attacks.
    """
    df = df.copy()
    df['time_diff'] = df['timestamp'].diff().fillna(0)
    
    mean_diff = df['time_diff'].mean()
    std_diff = df['time_diff'].std()
    
    df['z_score'] = (df['time_diff'] - mean_diff) / std_diff
    
    anomalies = df[np.abs(df['z_score']) > z_threshold]
    
    if not anomalies.empty:
        print(f"Detected {len(anomalies)} timestamp anomalies (Z-score > {z_threshold}).")
    
    return anomalies
