"""
Explainable Blockchain Anomaly Detection - Proof of Concept (MVP)
Author: Zebai Tian
Description: Full Pipeline - Data Loading, KH Interpolation, and Result Export.
"""
import pandas as pd
import numpy as np
import sys

def load_and_prepare_data(file_path):
    print("=====================================================")
    print("[SYSTEM] Initializing Explainable Anomaly Detection Engine")
    print("=====================================================")
    
    try:
        print(f"[INFO] Loading dataset from '{file_path}'...")
        df = pd.read_csv(file_path)
        print(f"[SUCCESS] Loaded {len(df)} transaction records.")
        
        print("[INFO] Normalizing core features (Min-Max Scaling)...")
        freq_col = 'Avg min between sent tnx'
        bal_col = 'total ether balance'
        
        freq_range = df[freq_col].max() - df[freq_col].min()
        bal_range = df[bal_col].max() - df[bal_col].min()
        
        df['Frequency_norm'] = (df[freq_col] - df[freq_col].min()) / (freq_range if freq_range > 0 else 1)
        df['Balance_norm'] = (df[bal_col] - df[bal_col].min()) / (bal_range if bal_range > 0 else 1)
        
        print("[SUCCESS] Feature normalization completed.")
        return df
        
    except FileNotFoundError:
        print(f"[ERROR] Could not find '{file_path}'. Please ensure it is in the current directory.")
        sys.exit(1)

def define_expert_rules():
    print("\n[INFO] Defining Expert Rule Anchors in 2D Feature Space...")
    # Danger: Fast frequency (0.0), Low balance (0.0)
    danger_anchor = {'freq': 0.0, 'bal': 0.0}
    # Safe: Slow frequency (1.0), High balance (1.0)
    safe_anchor = {'freq': 1.0, 'bal': 1.0}
    
    print(f"[RULES] High-Risk Anchor set at: Frequency={danger_anchor['freq']}, Balance={danger_anchor['bal']}")
    print(f"[RULES] Safe Anchor set at: Frequency={safe_anchor['freq']}, Balance={safe_anchor['bal']}")
    return danger_anchor, safe_anchor

def kh_distance_engine(df, danger_anchor, safe_anchor):
    """ Step 3: The Core KH Interpolation Engine """
    print("\n=====================================================")
    print("[SYSTEM] Executing Step 3: KH Distance Interpolation Engine")
    print("=====================================================")
    
    def calculate_risk(freq, bal):
        # Calculate Euclidean distance to Danger Anchor
        d_danger = np.sqrt((freq - danger_anchor['freq'])**2 + (bal - danger_anchor['bal'])**2)
        # Calculate Euclidean distance to Safe Anchor
        d_safe = np.sqrt((freq - safe_anchor['freq'])**2 + (bal - safe_anchor['bal'])**2)
        
        if d_danger + d_safe == 0: return 0.5
        
        # KH Inverse Distance Weighting: Closer to danger means higher risk score
        return d_safe / (d_danger + d_safe)
    
    print("[INFO] Calculating interpolated risk scores for all 9,841 transactions...")
    df['Risk_Score'] = df.apply(
        lambda row: calculate_risk(row['Frequency_norm'], row['Balance_norm']), 
        axis=1
    )
    print("[SUCCESS] KH Interpolation completed. 100% logical coverage achieved.")
    return df

def export_results(df):
    """ Step 4 & 5: Network Scanning and Exporting """
    print("\n=====================================================")
    print("[SYSTEM] Executing Step 4 & 5: Threat Detection & Export")
    print("=====================================================")
    
    # We define Risk Score > 0.85 as High-Risk Fraud
    threshold = 0.85
    print(f"[INFO] Scanning for high-risk accounts (Threshold: Risk Score >= {threshold})...")
    
    # Filter the suspects
    suspects = df[df['Risk_Score'] >= threshold].copy()
    # Sort them by risk score (Highest first)
    suspects = suspects.sort_values(by='Risk_Score', ascending=False)
    
    print(f"[ALERT] Detected {len(suspects)} high-risk fraudulent accounts!")
    
    print("\n[INFO] Top 5 Most Dangerous Accounts:")
    columns_to_export = ['Address', 'Avg min between sent tnx', 'total ether balance', 'Risk_Score', 'FLAG']
    print(suspects[columns_to_export].head(5).to_string(index=False))
    
    # Export to CSV
    output_file = 'High_Risk_Report.csv'
    suspects[columns_to_export].to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Final suspect list exported to '{output_file}'.")
    print("=====================================================")
    print("[SYSTEM] Explainable Anomaly Detection MVP - Terminated Successfully.")
    print("=====================================================")

if __name__ == "__main__":
    # 1. Load Data
    dataset = load_and_prepare_data('transaction_dataset.csv')
    
    # 2. Define Anchors
    danger_pt, safe_pt = define_expert_rules()
    
    # 3. Calculate Risk via KH Interpolation
    dataset_scored = kh_distance_engine(dataset, danger_pt, safe_pt)
    
    # 4 & 5. Export Suspects
    export_results(dataset_scored)