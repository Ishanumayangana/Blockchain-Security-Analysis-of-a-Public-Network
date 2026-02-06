import pandas as pd
import numpy as np

def detect_gas_anomalies(df):
    """
    Detects transactions with abnormal gas prices (potential spam or urgent prioritization).
    Returns DataFrame with 'z_score' and 'is_anomaly' columns.
    """
    if df.empty or 'gas_price' not in df.columns:
        return df
    
    mean_gas = df['gas_price'].mean()
    std_gas = df['gas_price'].std()
    
    if std_gas == 0:
        df['z_score'] = 0
    else:
        df['z_score'] = (df['gas_price'] - mean_gas) / std_gas
        
    df['is_anomaly'] = df['z_score'] > 2  # Flag if > 2 std dev
    return df

def detect_front_running(df):
    """
    Detects potential sandwich attacks: Large Buy -> Victim TX -> Large Sell
    in the same block.
    Returns a list of detected patterns.
    """
    suspicious_patterns = []
    
    if df.empty:
        return suspicious_patterns

    # Sort by block and index
    df_sorted = df.sort_values(['block_number', 'transaction_index'])
    
    # Simple heuristic for sandwich: High Gas Buy -> Normal -> High Gas Sell
    # In a real scenario, we'd check token transfers. Here we use gas price patterns.
    
    for block_num, group in df_sorted.groupby('block_number'):
        if len(group) < 3:
            continue
            
        txs = group.to_dict('records')
        for i in range(len(txs) - 2):
            t1 = txs[i]
            t2 = txs[i+1]
            t3 = txs[i+2]
            
            # Pattern: T1 & T3 have high gas, T2 has normal/lower gas
            # And T1/T3 are same sender (attacker) - simplified for simulation
            if (t1['gas_price'] > t2['gas_price'] * 1.5 and 
                t3['gas_price'] > t2['gas_price'] * 1.5):
                
                suspicious_patterns.append({
                    'block': block_num,
                    'attacker_tx_1': t1['hash'],
                    'victim_tx': t2['hash'],
                    'attacker_tx_2': t3['hash'],
                    'gas_price_spike': t1['gas_price'] - t2['gas_price']
                })
                
    return suspicious_patterns
