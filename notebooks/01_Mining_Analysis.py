# %% [markdown]
# # Module 1: 51% Attack & Mining Analysis
# This notebook demonstrates how to detect mining centralization and timestamp anomalies.

# %%
import sys
import os
sys.path.append('..') # Add parent directory to path to import src

from src.data_loader import generate_synthetic_mining_data
from src.attacks.mining_attack import calculate_miner_metrics, detect_51_percent_attack, calculate_gini_coefficient, detect_timestamp_manipulation
from src.utils import setup_plotting_style, plot_miner_distribution, plot_block_times

setup_plotting_style()

# %% [markdown]
# ## 1. Generate Data
# We will generate synthetic data simulating a scenario where one miner controls a large portion of the hashrate.

# %%
# Generate normal data
# df = generate_synthetic_mining_data(num_blocks=500, attack_scenario=False)

# Generate attack data
df_attack = generate_synthetic_mining_data(num_blocks=500, attack_scenario=True)
print(df_attack.head())

# %% [markdown]
# ## 2. Analyze Miner Centralization
# We calculate the share of blocks mined by each address.

# %%
miner_stats = calculate_miner_metrics(df_attack)
print(miner_stats)

plot_miner_distribution(df_attack, title="Miner Distribution (Attack Scenario)")

# %% [markdown]
# ## 3. Detect 51% Attack
# Check if any miner breaches the 50% threshold.

# %%
attackers = detect_51_percent_attack(miner_stats, threshold=0.50)

# %% [markdown]
# ## 4. Gini Coefficient
# A higher Gini coefficient indicates higher centralization.

# %%
gini = calculate_gini_coefficient(miner_stats)
print(f"Mining Gini Coefficient: {gini:.4f}")

# %% [markdown]
# ## 5. Timestamp Analysis
# Detect anomalies in block production times.

# %%
plot_block_times(df_attack)
anomalies = detect_timestamp_manipulation(df_attack)
print("Anomalies detected at blocks:")
print(anomalies[['block_number', 'timestamp', 'time_diff', 'z_score']])
