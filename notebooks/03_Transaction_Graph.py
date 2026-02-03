# %% [markdown]
# # Module 3: Sybil Attack & Network Analysis
# This notebook analyzes transaction graphs to detect Sybil attacks and money laundering patterns.

# %%
import sys
sys.path.append('..') 

from src.data_loader import generate_synthetic_transaction_network
from src.attacks.network_analysis import build_transaction_graph, analyze_network_metrics, detect_sybil_communities, plot_transaction_graph
from src.utils import setup_plotting_style
import networkx as nx

setup_plotting_style()

# %% [markdown]
# ## 1. Generate Transaction Data
# We generate a network with a "Sybil Cluster" - a group of accounts created by one entity interacting closely.

# %%
df = generate_synthetic_transaction_network(num_tx=500, sybil_scenario=True)
print(df.head())

# %% [markdown]
# ## 2. Build Graph
# Construct a directed graph from the transactions.

# %%
G = build_transaction_graph(df)
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# %% [markdown]
# ## 3. Analyze Metrics
# Calculate centrality and clustering. High clustering may indicate a tight-knit community (or Sybil ring).

# %%
metrics = analyze_network_metrics(G)
# Show top nodes by clustering coefficient
print(metrics.sort_values('clustering_coefficient', ascending=False).head(10))

# %% [markdown]
# ## 4. Detect Sybil Clusters
# We use community detection and clustering heuristics to find suspicious groups.

# %%
clusters = detect_sybil_communities(G)
suspicious_nodes = []
print(f"Detected {len(clusters)} potentially suspicious clusters.")

for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: Size {cluster['size']}, Avg Clustering {cluster['avg_clustering']:.2f}")
    suspicious_nodes.extend(cluster['members'])

# %% [markdown]
# ## 5. Visualization
# Plot the network. Red nodes are part of suspicious clusters.

# %%
plot_transaction_graph(G, suspicious_nodes=suspicious_nodes, title="Sybil Attack Detection")
