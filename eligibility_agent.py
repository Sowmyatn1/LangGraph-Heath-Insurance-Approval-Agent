# src/eligibility_agent.py
import pandas as pd
from langchain.chat_models import init_chat_model
from data_loader import load_data
import os
from dotenv import load_dotenv
load_dotenv()
import json

"""
This module checks the eligibility of a claim using patient info, claim info, and insurance rules.you are creating data frames with all the 
data from csv and passing it to the LLM to make a decision on whether the claim is eligible or not.the response from LLM is Json
"""
# Load all data
data_store = load_data()
patients_df = data_store["patients"]
claims_df = data_store["claims"]
rules_df = data_store["rules"]

# STEP 1: Initialize Gemini LLM
llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.5,
    api_key=os.getenv("GOOGLE_API_KEY")
)

def eligibility_agent(claim_id: str):
    """Check eligibility of a claim using patient info, claim info, and insurance rules"""

    # 1. Get claim
    claim = claims_df[claims_df["claim_id"] == claim_id]
    if claim.empty:
        return f"Claim ID {claim_id} not found"
    claim = claim.iloc[0].to_dict()

    # 2. Get patient
    patient = patients_df[patients_df["patient_id"] == claim["patient_id"]]
    if patient.empty:
        return f"Patient ID {claim['patient_id']} not found"
    patient = patient.iloc[0].to_dict()

    # 3. Get insurance rule
    plan_id = patient.get("plan_id")
    procedure_code = claim["procedure_code"]
    rule = rules_df[
        (rules_df["plan_id"] == plan_id) & 
        (rules_df["procedure_code"] == procedure_code)
    ]
    if rule.empty:
        return f"No insurance rule found for plan {plan_id} and procedure {procedure_code}"
    rule = rule.iloc[0].to_dict()

    # 4. Create prompt for Gemini
    prompt = f"""
    You are an insurance eligibility checker.

    Claim Info:
    #{claim}

    #{patient}

    Insurance Rule:
    #{rule}

    Task:
    - Decide if this claim is eligible for coverage.
    - Check patient age, gender, plan, and procedure rules.
    - Include whether prior authorization is required.
    - Return the result in JSON with keys:
      {{
        "eligible": true/false,
        "reason": "explanation",
        "prior_auth_required": true/false
      }}
    """

    # 5. Invoke Gemini
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        # fallback if LLM doesn't return valid JSON
        result = {"eligible": False, "reason": response.content.strip(), "prior_auth_required": False}
    
    return result

"""
# Test the agent
if __name__ == "__main__":
    test_claim_id = "C20003"  # Example from claims.csv
    result = eligibility_agent(test_claim_id)
    print(f"Eligibility result for claim {test_claim_id}: {result}")
"""