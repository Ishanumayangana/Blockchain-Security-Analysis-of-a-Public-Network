# Blockchain Security Analysis of a Public Network

## Overview
This project provides a comprehensive toolkit for analyzing security threats in public blockchains (Ethereum/Bitcoin). It combines traditional graph theory with Machine Learning to detect anomalies, smart contract vulnerabilities, and network attacks.

The project features a **modern Web Interface** built with Streamlit for interactive analysis and visualization.

## 🛡️ Key Features

### 1. Consensus Security (51% Attack)
- **Detection**: Analyzes hashrate distribution to identify centralization.
- **Anomaly Detection**: Uses Z-score analysis to flag timestamp manipulation in block production.
- **Simulation**: Interactive scenarios to simulate an attacker gaining majority control.

### 2. Smart Contract Security
- **ML Classifier**: A Random Forest model trained to detect Reentrancy vulnerabilities.
- **Feature Analysis**: Evaluates dangerous patterns like unchecked external calls and missing guards.
- **Risk Scoring**: Provides a probability score for contract vulnerability.

### 3. Network Forensics (Sybil Attack)
- **Graph Analysis**: visualizes transaction flows using `networkx`.
- **Sybil Detection**: Identifies suspicious clusters of accounts with high clustering coefficients.
- **Visualization**: Interactive 2D graph with legend distinguishing normal vs. suspicious nodes.

### 4. Gas Monitor & MEV Detection (New)
- **Sandwich Attacks**: Detects front-running patterns where bots exploit user trades.
- **Gas Anomalies**: Identifies transactions with abnormal gas prices (>2 standard deviations).
- **Reporting**: Export analysis results to CSV for external auditing.

## 💻 Web Interface
A professional, light-themed dashboard allows you to run simulations and view results in real-time.

**Credentials:**
- No default credentials required (Demo Mode active).
- *Optional*: Default `admin` / `admin` if authentication re-enabled.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
Launch the interactive dashboard:
```bash
python -m streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

### Project Structure
- `app.py`: Main entry point for the Web Interface.
- `src/`: Core analysis logic.
    - `attacks/`: Modules for Mining, Contracts, and Network analysis.
    - `ui/`: Authentication and Styling assets.
    - `data_loader.py`: Synthetic data generation and web3 connection.
    - `gas_analysis.py`: Gas price and MEV detection logic.
- `notebooks/`: Jupyter notebooks for standalone research and prototyping.

## 📊 Technologies Used
- **Python**: Core logic.
- **Streamlit**: Web UI framework.
- **Pandas/NumPy**: Data processing.
- **Scikit-learn**: Machine Learning models.
- **NetworkX**: Graph theory and analysis.
- **Plotly**: Interactive charts and graph visualization.
