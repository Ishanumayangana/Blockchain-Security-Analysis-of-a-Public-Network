
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Import our custom modules
from src.ui.auth import simple_login
import src.data_loader as dl
import src.attacks.mining_attack as ma
import src.attacks.contract_vuln as cv
import src.attacks.network_analysis as na

# --- CACHED FUNCTIONS ---
@st.cache_data
def get_mining_data(num_blocks, attack_scenario):
    return dl.generate_synthetic_mining_data(num_blocks, attack_scenario)

@st.cache_data
def get_contract_data(n_samples):
    return dl.generate_synthetic_contract_data(n_samples)

@st.cache_data
def get_train_model():
    df = get_contract_data(1000)
    model, _, _, _ = cv.train_vulnerability_classifier(df)
    return model

@st.cache_data
def get_transaction_data(num_tx, sybil_scenario):
    return dl.generate_synthetic_transaction_network(num_tx, sybil_scenario)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Blockchain Security Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
with open('src/ui/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- AUTHENTICATION ---
if not simple_login():
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 🛡️ Security Suite")
    selected = option_menu(
        menu_title=None,
        options=["Home", "51% Attack", "Smart Contract Ops", "Network Forensics"],
        icons=["house", "cpu", "file-code", "diagram-3"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00ADB5", "font-size": "16px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#393E46"},
            "nav-link-selected": {"background-color": "#00ADB5"},
        }
    )
    st.markdown("---")
    st.info("System Status: Online 🟢")

# --- PAGE: HOME ---
if selected == "Home":
    st.title("Blockchain Security Analysis Suite")
    st.markdown("### Public Network Anomaly Detection System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div data-testid="metric-container">
                <h3>🔍 Mining Analysis</h3>
                <p>Detect 51% attacks and timestamp manipulation in PoW/PoS networks.</p>
            </div>
            """, unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div data-testid="metric-container">
                <h3>📜 Contract Security</h3>
                <p>ML-based detection of Reentrancy and Logic Vulnerabilities.</p>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            """
            <div data-testid="metric-container">
                <h3>🕸️ Network Forensics</h3>
                <p>Graph theory analysis to identify Sybil clusters and money laundering.</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("#### Recent Alerts")
    st.warning("⚠️ High Mining Centralization detected (Gini > 0.7)")
    st.info("ℹ️ 5 suspicious Sybil clusters identified in last scan.")

# --- PAGE: 51% ATTACK ---
elif selected == "51% Attack":
    st.title("⛏️ Consensus Security: 51% Attack Analysis")
    
    tab1, tab2 = st.tabs(["📊 Live Monitoring", "⚙️ Simulation Settings"])
    
    with tab2:
        st.subheader("Simulation Parameters")
        attack_sim = st.checkbox("Simulate Attack Scenario", value=True)
        blocks_to_fetch = st.slider("Blocks to Analyze", 100, 2000, 500)
    
    with tab1:
        # Load Data
        with st.spinner('Fetching Blockchain Data...'):
            df = get_mining_data(blocks_to_fetch, attack_sim)
            miner_stats = ma.calculate_miner_metrics(df)
            gini = ma.calculate_gini_coefficient(miner_stats)
        
        # Top Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Blocks", len(df))
        m2.metric("Active Miners", len(miner_stats))
        m3.metric("Gini Coefficient", f"{gini:.4f}", delta_color="inverse")
        
        # Attack Detection
        attackers = ma.detect_51_percent_attack(miner_stats)
        if attackers:
            st.error(f"🚨 **CRITICAL ALERT**: 51% Threshold Breached by: {', '.join(attackers)}")
        else:
            st.success("✅ Network Decentralization is Healthy")

        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.markdown("### Hashrate Distribution")
            fig = px.pie(miner_stats, values='blocks_mined', names=miner_stats.index, 
                         title="Miner Block Share", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig, use_container_width=True)
            
        with col_viz2:
            st.markdown("### Block Production Times")
            df['time_diff'] = df['timestamp'].diff()
            fig_time = px.line(df, x='block_number', y='time_diff', title="Block Time Intervals (s)")
            fig_time.update_traces(line_color='#00ADB5')
            st.plotly_chart(fig_time, use_container_width=True)
            
        # Timestamp Anomalies
        anomalies = ma.detect_timestamp_manipulation(df)
        if not anomalies.empty:
            st.subheader(f"⚠️ Timestamp Anomalies Detected ({len(anomalies)})")
            st.dataframe(anomalies[['block_number', 'timestamp', 'time_diff', 'z_score']].head(), use_container_width=True)

# --- PAGE: SMART CONTRACTS ---
elif selected == "Smart Contract Ops":
    st.title("📜 Smart Contract Vulnerability Scanner")
    
    st.markdown("Predict vulnerability utilizing **Random Forest Classification** on bytecode features.")
    
    col_input, col_res = st.columns([1, 2])
    
    with col_input:
        st.subheader("Contract Parameters")
        has_ext = st.checkbox("Makes External Calls?", value=True)
        state_chg = st.checkbox("State Change After Call?", value=True)
        no_guard = st.checkbox("Missing Reentrancy Guard?", value=True)
        del_call = st.checkbox("Uses DelegateCall?", value=False)
        complexity = st.slider("Code Complexity Score", 1, 100, 50)
        
        analyze_btn = st.button("Analyze Contract Risk")
        
    with col_res:
        if analyze_btn:
            # Train model on fly (demo purposes)
            with st.spinner("Analyzing..."):
                model = get_train_model()
                
                # Predict
                input_df = pd.DataFrame([{
                    'has_external_call': int(has_ext),
                    'state_change_after_call': int(state_chg),
                    'no_reentrancy_guard': int(no_guard),
                    'uses_delegatecall': int(del_call),
                    'code_complexity': complexity
                }])
                
                prob = model.predict_proba(input_df)[0][1]
                
                st.subheader("Risk Assessment")
                if prob > 0.7:
                    st.error(f"🔴 **VULNERABLE** (Confidence: {prob:.1%})")
                    st.markdown("**Identified Risks:**\n- Reentrancy Pattern Detected\n- Unsafe External Call Flow")
                elif prob > 0.3:
                    st.warning(f"🟡 **SUSPICIOUS** (Confidence: {prob:.1%})")
                else:
                    st.success(f"🟢 **SAFE** (Confidence: {1-prob:.1%})")
                    
                # Feature Importance
                st.markdown("#### Model Decision Factors")
                feat_imp = pd.DataFrame({
                    'Feature': input_df.columns,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False)
                st.bar_chart(feat_imp.set_index('Feature'))

# --- PAGE: NETWORK ANALYSIS ---
elif selected == "Network Forensics":
    st.title("🕸️ Transaction Network Forensics")
    
    st.info("Visualizing transaction flows to detect Sybil rings and money laundering patterns.")
    
    with st.expander("Configuration", expanded=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            tx_count = st.slider("Transaction Count", 100, 1000, 300)
        with col_c2:
            sybil_mode = st.checkbox("Inject Sybil Attack Scenario", value=True)
            
    # Compute
    df_tx = get_transaction_data(tx_count, sybil_mode)
    G = na.build_transaction_graph(df_tx)
    metrics = na.analyze_network_metrics(G)
    clusters = na.detect_sybil_communities(G)
    
    # --- LAYOUT SPLIT ---
    col_graph, col_details = st.columns([3, 1])
    
    with col_details:
        st.subheader("📊 Analysis Metrics")
        st.metric("Total Nodes", G.number_of_nodes())
        st.metric("Total Edges", G.number_of_edges())
        st.metric("Suspicious Clusters", len(clusters), delta_color="inverse")
        
        st.markdown("---")
        st.markdown("#### ℹ️ Guide")
        st.caption("**Clustering Coefficient**: Measures how connected a node's neighbors are. High values (near 1.0) in transaction networks often indicate artificial rings (Sybil behavior).")
        
        st.markdown("**Legend:**")
        st.markdown("🔵 **Normal Account**")
        st.markdown("🔴 **Suspicious / Sybil**")

    # Visualization using NetworkX + Plotly
    pos = nx.spring_layout(G, seed=42)
    
    # Extract suspicious nodes and build legend groups
    suspicious_nodes = set()
    for c in clusters:
        suspicious_nodes.update(c['members'])
        
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name='Transactions'
    )

    # Split nodes into two traces for properly labeled legend
    normal_x, normal_y, normal_text = [], [], []
    sybil_x, sybil_y, sybil_text = [], [], []
    
    for node in G.nodes():
        x, y = pos[node]
        if node in suspicious_nodes:
            sybil_x.append(x)
            sybil_y.append(y)
            sybil_text.append(f"Suspicious Node: {node}")
        else:
            normal_x.append(x)
            normal_y.append(y)
            normal_text.append(f"Account: {node}")

    normal_nodes = go.Scatter(
        x=normal_x, y=normal_y,
        mode='markers',
        hoverinfo='text',
        text=normal_text,
        name='Normal Account',
        marker=dict(size=10, color='#00ADB5', line_width=1)
    )
    
    sybil_nodes = go.Scatter(
        x=sybil_x, y=sybil_y,
        mode='markers',
        hoverinfo='text',
        text=sybil_text,
        name='Sybil / Suspicious',
        marker=dict(size=12, color='#FF4B4B', line_width=2, symbol='diamond')
    )

    fig_net = go.Figure(data=[edge_trace, normal_nodes, sybil_nodes],
             layout=go.Layout(
                title=dict(text='Transaction Network Graph', font=dict(size=16)),
                showlegend=True,
                legend=dict(x=0, y=1),
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    
    with col_graph:
        st.plotly_chart(fig_net, use_container_width=True)
    
    # Detailed Table below
    if clusters:
        st.markdown("### 🕵️ Detected Sybil Clusters Details")
        cluster_data = []
        for i, c in enumerate(clusters):
            cluster_data.append({
                "Cluster ID": i+1,
                "Size": len(c['members']),
                "Avg Clustering Coeff": f"{c['avg_clustering']:.2f}",
                "Members": ", ".join(list(c['members'])[:5]) + ("..." if len(c['members']) > 5 else "")
            })
        st.table(pd.DataFrame(cluster_data))

