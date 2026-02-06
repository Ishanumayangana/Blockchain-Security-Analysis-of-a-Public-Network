import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def build_transaction_graph(df):
    """
    Builds a directed graph from transaction data.
    """
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row['from_address'], row['to_address'], weight=row['value'])
    return G

def analyze_network_metrics(G):
    """
    Calculates centrality and clustering metrics.
    """
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Clustering coefficient for directed graphs requires converting to undirected or using specific algos.
    # We'll treat as undirected for clustering to see local connectivity.
    G_undir = G.to_undirected()
    clustering_coeffs = nx.clustering(G_undir)
    
    metrics = pd.DataFrame({
        'degree_centrality': degree_centrality,
        'betweenness_centrality': betweenness_centrality,
        'clustering_coefficient': clustering_coeffs
    })
    return metrics

def detect_sybil_communities(G, min_size=3, clustering_threshold=0.5):
    """
    Detects potential Sybil clusters based on high clustering coefficient and density.
    Sybils often communicate heavily amongst themselves.
    """
    G_undir = G.to_undirected()
    communities = list(nx.community.greedy_modularity_communities(G_undir))
    
    suspicious_clusters = []
    
    for com in communities:
        if len(com) < min_size:
            continue
            
        subgraph = G_undir.subgraph(com)
        avg_clustering = nx.average_clustering(subgraph)
        
        # Heuristic: High clustering often indicates artificial structures (Sybils)
        if avg_clustering > clustering_threshold:
            suspicious_clusters.append({
                'members': list(com),
                'avg_clustering': avg_clustering,
                'size': len(com)
            })
            
    return suspicious_clusters

def plot_transaction_graph(G, suspicious_nodes=None, title="Transaction Network"):
    """
    Plots the graph, highlighting suspicious nodes if provided.
    """
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    
    node_colors = ['blue' if node not in (suspicious_nodes or []) else 'red' for node in G.nodes()]
    
    nx.draw_networkx(G, pos, 
                     node_color=node_colors, 
                     with_labels=False, 
                     node_size=50, 
                     alpha=0.7, 
                     edge_color='gray',
                     arrowsize=10)
    
    if suspicious_nodes:
        # Draw labels only for suspicious nodes
        labels = {node: node for node in suspicious_nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='black')
        
    plt.title(title)
    plt.axis('off')
    plt.show()
