import pandas as pd
import numpy as np

def analyze_audit_status():
    print("--- Analyzing audit_status ---")
    df = pd.read_csv('test_audit/audit_status_sample.txt', sep='|')
    
    # Replace 'NULL' strings with NaN
    df.replace('NULL', np.nan, inplace=True)
    
    # Convert to datetime
    for col in df.columns:
        if 'DATE' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # For each claim, order the non-null dates and find the sequence
    sequences = []
    for index, row in df.iterrows():
        # Get dictionary of non-null dates
        dates = {col: row[col] for col in df.columns if pd.notnull(row[col])}
        if len(dates) > 1:
            # Sort by date
            sorted_dates = sorted(dates.items(), key=lambda item: item[1])
            seq = " -> ".join([item[0] for item in sorted_dates])
            sequences.append(seq)
            
    seq_series = pd.Series(sequences)
    print("Most common sequences in audit_status:")
    print(seq_series.value_counts().head(10))

def analyze_claim_intimation():
    print("\n--- Analyzing claim_intimation ---")
    df = pd.read_csv('test_audit/claim_intimation_sample.txt', sep='|')
    
    df.replace('NULL', np.nan, inplace=True)
    
    for col in df.columns:
        if 'DATE' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    sequences = []
    for index, row in df.iterrows():
        dates = {col: row[col] for col in df.columns if pd.notnull(row[col])}
        if len(dates) > 1:
            sorted_dates = sorted(dates.items(), key=lambda item: item[1])
            seq = " -> ".join([item[0] for item in sorted_dates])
            sequences.append(seq)
            
    seq_series = pd.Series(sequences)
    print("Most common sequences in claim_intimation:")
    print(seq_series.value_counts().head(10))

if __name__ == "__main__":
    analyze_audit_status()
    analyze_claim_intimation()
