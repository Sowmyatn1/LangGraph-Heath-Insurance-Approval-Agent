# src/explanation_agent.py
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

"""
This module explains the decision of the claim workflow to a claims officer.it collects the results from all the other agents and 
produces a human-readable explanation with policy references.
"""
# Initialize Gemini
llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.7,
    api_key=os.getenv("GOOGLE_API_KEY")
)

def explanation_agent(workflow_result: dict):
    """
    Take workflow results and produce a human-readable explanation with policy references.
    """

    claim_id = workflow_result.get("claim_id")
    status = workflow_result.get("status")
    validation = workflow_result.get("validation_result", {})
    eligibility = workflow_result.get("eligibility_result", {})
    policy = workflow_result.get("policy_response", "")
    fraud = workflow_result.get("fraud_result", {})

    prompt = f"""
    You are an expert insurance claims explainer. 
    Summarize the claim decision for a claims officer in plain English.

    Claim ID: {claim_id}
    Final Status: {status}

    Validation Result: {validation}
    Eligibility Result: {eligibility}
    Policy Reference: {policy}
    Fraud Result: {fraud}

    Task:
    - Explain the decision in a clear, human-friendly way.
    - Cite relevant policy document snippets from the Policy Reference section.
    - Provide both the decision and supporting justification.
    - Keep it professional and concise.
    """

    response = llm.invoke(prompt)
    print("this is from explanination agent:::",response.content.strip())
    return response.content.strip()
