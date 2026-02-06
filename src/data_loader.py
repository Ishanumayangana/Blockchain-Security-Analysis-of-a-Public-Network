import pandas as pd
import numpy as np
from web3 import Web3
import random
import time

def connect_web3(rpc_url=None):
    """
    Connects to a Web3 provider.
    If rpc_url is None, tries to connect to a local node or public endpoint.
    """
    if not rpc_url:
        # Example public RPC (Mainnet) - Note: Rate limits may apply
        rpc_url = "https://cloudflare-eth.com"
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if w3.is_connected():
        print(f"Connected to Web3 at {rpc_url}")
        return w3
    else:
        print("Failed to connect to Web3")
        return None

def fetch_block_data(w3, start_block, num_blocks=100):
    """
    Fetches real block data from the blockchain.
    Returns a DataFrame.
    """
    data = []
    try:
        if start_block == 'latest':
            start_block = w3.eth.block_number
        
        for i in range(num_blocks):
            block_num = start_block - i
            block = w3.eth.get_block(block_num)
            data.append({
                'block_number': block['number'],
                'timestamp': block['timestamp'],
                'miner': block['miner'],
                'difficulty': block.get('difficulty', 0), # Difficulty might be 0 on PoS
                'gas_used': block['gasUsed'],
                'gas_limit': block['gasLimit'],
                'tx_count': len(block['transactions'])
            })
            if i % 10 == 0:
                print(f"Fetched block {block_num}...")
                
    except Exception as e:
        print(f"Error fetching blocks: {e}")
    
    return pd.DataFrame(data)

def generate_synthetic_mining_data(num_blocks=1000, attack_scenario=False):
    """
    Generates synthetic block data to simulate mining behavior.
    If attack_scenario is True, simulates a 51% attack by one miner.
    """
    print("Generating synthetic mining data...")
    miners = [f"0xMiner{i}" for i in range(10)]
    
    data = []
    current_time = int(time.time())
    
    # Normal distribution of hash power
    miner_weights = [0.1] * 10
    
    if attack_scenario:
        # One miner gets 55% of the hash power
        miner_weights = [0.05] * 9 + [0.55]
        
    for i in range(num_blocks):
        chosen_miner = np.random.choice(miners, p=miner_weights)
        
        # Block time usually ~12-14s for Eth PoW, or 12s fixed for PoS
        time_diff = int(np.random.normal(12, 2)) 
        current_time -= time_diff
        
        data.append({
            'block_number': 1000000 + i,
            'timestamp': current_time,
            'miner': chosen_miner,
            'difficulty': 5000000000 + int(np.random.normal(0, 10000)),
            'gas_used': int(np.random.uniform(1000000, 30000000)),
            'tx_count': int(np.random.randint(50, 300))
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp')
    return df

def generate_synthetic_transaction_network(num_tx=500, sybil_scenario=False):
    """
    Generates a synthetic transaction list for network analysis.
    """
    print("Generating synthetic transaction network...")
    accounts = [f"0xUser{i}" for i in range(50)]
    data = []
    
    df = pd.DataFrame({
        'from_address': [f"0x{np.random.randint(100, 999)}" for _ in range(num_tx)],
        'to_address': [f"0x{np.random.randint(100, 999)}" for _ in range(num_tx)],
        'value': np.random.exponential(1.5, num_tx),
        'block_number': np.random.randint(100000, 100010, num_tx),
        'transaction_index': np.random.randint(0, 50, num_tx),
        'gas_price': np.random.normal(20, 5, num_tx), # Gwei
        'hash': [f"0xTx{i}" for i in range(num_tx)]
    })
    
    # Inject Sybil Patterns
    if sybil_scenario:
        # Create a "Ring" of transactions
        sybil_accounts = [f"0xSybil{i}" for i in range(5)]
        for i in range(len(sybil_accounts)):
            df = pd.concat([df, pd.DataFrame([{
                'from_address': sybil_accounts[i],
                'to_address': sybil_accounts[(i+1) % len(sybil_accounts)],
                'value': 10.0,
                'block_number': 100005,
                'transaction_index': 100+i,
                'gas_price': 20.0,
                'hash': f"0xSybilTx{i}"
            }])], ignore_index=True)
            
    # Inject Front-Running (Sandwich) Patterns
    # High Gas Buy -> Victim -> High Gas Sell
    attacker = "0xMEVBot"
    victim = "0xVictim"
    
    sandwich_block = 100008
    
    # Front-run (Buy)
    df = pd.concat([df, pd.DataFrame([{
        'from_address': attacker, 'to_address': "0xDex", 'value': 50,
        'block_number': sandwich_block, 'transaction_index': 1, 'gas_price': 150.0, 'hash': "0xSandwichBuy"
    }])], ignore_index=True)
    
    # Victim
    df = pd.concat([df, pd.DataFrame([{
        'from_address': victim, 'to_address': "0xDex", 'value': 5,
        'block_number': sandwich_block, 'transaction_index': 2, 'gas_price': 50.0, 'hash': "0xVictimTx"
    }])], ignore_index=True)
    
    # Back-run (Sell)
    df = pd.concat([df, pd.DataFrame([{
        'from_address': attacker, 'to_address': "0xDex", 'value': 50,
        'block_number': sandwich_block, 'transaction_index': 3, 'gas_price': 140.0, 'hash': "0xSandwichSell"
    }])], ignore_index=True)

    return df

def generate_synthetic_contract_data(n_samples=1000):
    """
    Generates synthetic dataset of smart contract features and vulnerability labels.
    Features logic:
    - has_external_call: 1 if contract calls external address
    - state_change_after_call: 1 if state is modified after external call (Reentrancy risk)
    - no_reentrancy_guard: 1 if 'nonReentrant' modifier is missing
    - uses_delegatecall: 1 if delegatecall is used (High risk)
    """
    np.random.seed(42)
    
    # Generate random features
    has_external_call = np.random.randint(0, 2, n_samples)
    state_change_after_call = np.random.randint(0, 2, n_samples)
    no_reentrancy_guard = np.random.randint(0, 2, n_samples)
    uses_delegatecall = np.random.randint(0, 2, n_samples)
    code_complexity = np.random.randint(1, 100, n_samples)
    
    # Logic for labeling vulnerabilities (simulating ground truth)
    # Reentrancy: call + state change after call + no guard
    is_vulnerable = (
        (has_external_call == 1) & 
        (state_change_after_call == 1) & 
        (no_reentrancy_guard == 1)
    )
    
    # Add some noise/other bugs (e.g. delegatecall risks)
    is_vulnerable = is_vulnerable | (uses_delegatecall == 1)
    
    # Add random noise to simulate real-world imperfection
    noise = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])
    labels = np.bitwise_xor(is_vulnerable.astype(int), noise)
    
    df = pd.DataFrame({
        'has_external_call': has_external_call,
        'state_change_after_call': state_change_after_call,
        'no_reentrancy_guard': no_reentrancy_guard,
        'uses_delegatecall': uses_delegatecall,
        'code_complexity': code_complexity,
        'vulnerable': labels
    })
    
    return df
