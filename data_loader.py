# src/data_loader.py
import pandas as pd
"""
This module loads the insurance data from the CSV files.
"""
def load_data():
    patients_df = pd.read_csv("data/patients.csv")
    claims_df = pd.read_csv("data/claims.csv")
    rules_df = pd.read_csv("data/insurance_rules.csv")

# Optional: expose as dictionary
    return {
        "patients": patients_df,
        "claims": claims_df,
        "rules": rules_df
    }
