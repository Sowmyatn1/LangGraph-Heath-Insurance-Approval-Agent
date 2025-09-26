
"""
This file we are performing the initial validations for the claims.
once the inital validation will pass next step is to check the eligibility
"""
import pandas as pd
from datetime import datetime
from data_loader import load_data



"""Check validate the mandatory fileds in the claims.csv if any filed is missing in the csv file """
def validate_mandatory_fields(claim):
    """Check if all required fields are present and not empty"""
    required_fields = [
        "claim_id", "patient_id", "procedure_code", "diagnosis_code",
        "claim_amount", "date", "provider"
    ]
    missing_or_empty = [
        f for f in required_fields
        if pd.isna(claim.get(f)) or str(claim.get(f)).strip() == ""
    ]
    if missing_or_empty:
        return False, f"Missing or empty mandatory fields: {', '.join(missing_or_empty)}"
    return True, None

"""Check if the patient_id in the claims.csv exists in the patients.csv file"""

def validate_patient_id(claim, patients_df):
    """Check if patient ID exists in the patient records"""
    patient_id = claim["patient_id"]
    if not (patients_df["patient_id"] == patient_id).any():
        return False, f"Patient ID {patient_id} not found"
    return True, None

"""Check if the procedure_code and diagnosis_code in the claims.csv file are valid"""

def validate_claimamount(claim):
    """Check if claim amount is positive"""
    if claim["claim_amount"] <= 0:
        return False, f"Invalid claim amount: {claim['claim_amount']}"
    return True, None

def validate_codes(claim):
    """Simple validation for CPT/HCPCS and ICD-10 codes"""
    proc = str(claim["procedure_code"])
    diag = str(claim["diagnosis_code"])

    if not (proc.startswith("CPT_") or proc.startswith("HCPCS_")):
        return False, f"Invalid procedure code: {proc}"
    if not diag.startswith("ICD10_"):
        return False, f"Invalid diagnosis code: {diag}"
    return True, None

def validate_claims(claim_id):
    """Run all validation checks on claims"""
    data_store = load_data()
    claims_df = data_store["claims"]
    patients_df = data_store["patients"]

    errors = []


    # Get this specific claim
    claim_row = claims_df[claims_df["claim_id"] == claim_id]
    if claim_row.empty:
        return {"valid": False, "error": f"Claim {claim_id} not found"}

    claim_dict = claim_row.iloc[0].to_dict()

    # Mandatory checks
    ok, msg = validate_mandatory_fields(claim_dict)
    if not ok:
        return {"valid": False, "error": msg}

    # Code checks
    ok, msg = validate_codes(claim_dict)
    if not ok:
        return {"valid": False, "error": msg}

    # Logical checks
    ok, msg = validate_patient_id(claim_dict, patients_df)
    if not ok:
        return {"valid": False, "error": msg}
    
    ok, msg = validate_claimamount(claim_dict)
    if not ok:
        return {"valid": False, "error": msg}

    return {"valid": True, "error": None}

"""
if __name__ == "__main__":
    test_claim_id = "C20003"  # pick one from claims.csv
    result = validate_claims(test_claim_id)
    print(f"Validation result for claim {test_claim_id}: {result}")
"""