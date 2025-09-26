# src/fraud_detection_agent.py
import pandas as pd
from data_loader import load_data

# Load data
data_store = load_data()
claims_df = data_store["claims"]

"""
This module detects potential fraud in claims using claim amounts, patterns, and thresholds.
"""
# Define thresholds for fraud detection
HIGH_BILLED_AMOUNT = 50000  # Example threshold for unusually high claim
ANOMALOUS_THRESHOLD_FACTOR = 3  # For statistical outliers

def fraud_agent(claim_id):
    """Check for potential fraud in a single claim."""
    
    claim_row = claims_df[claims_df["claim_id"] == claim_id]
    if claim_row.empty:
        return {"claim_id": claim_id, "fraud_flag": False, "reason": "Claim not found"}

    claim = claim_row.iloc[0].to_dict()
    fraud_flags = []

    # 1. High billed amount
    if claim["claim_amount"] > HIGH_BILLED_AMOUNT:
        fraud_flags.append(f"High billed amount: ${claim['claim_amount']}")

    # 2. Duplicate claims
    duplicates = claims_df[
        (claims_df["patient_id"] == claim["patient_id"]) &
        (claims_df["procedure_code"] == claim["procedure_code"]) &
        (claims_df["provider"] == claim["provider"]) &
        (claims_df["date"] == claim["date"]) &
        (claims_df["claim_id"] != claim_id)
    ]
    if not duplicates.empty:
        fraud_flags.append(f"Duplicate claim(s) found: {', '.join(duplicates['claim_id'].tolist())}")

    # 3. Anomalous patterns (using simple z-score on claim_amount)
    #The average claim amount across all claims.
    mean_amount = claims_df["claim_amount"].mean()
    #The standard deviation of claim amounts.
    std_amount = claims_df["claim_amount"].std()
    #This calculates how far the claim’s amount is from the average:
    if abs(claim["claim_amount"] - mean_amount) > ANOMALOUS_THRESHOLD_FACTOR * std_amount:
        fraud_flags.append(f"Anomalous claim amount: ${claim['claim_amount']} (mean: ${mean_amount:.2f})")

    if fraud_flags:
        return {
            "claim_id": claim_id,
            "fraud_flag": True,
            "reason": "; ".join(fraud_flags)
        }
    else:
        return {"claim_id": claim_id, "fraud_flag": False, "reason": None}

"""
# Example test
if __name__ == "__main__":
    test_claim_id = "C20003"
    result = fraud_agent(test_claim_id)
    print("Fraud Check Result:", result)
"""