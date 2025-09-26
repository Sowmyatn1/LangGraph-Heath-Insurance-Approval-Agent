# src/langgraph_workflow.py
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from data_loader import load_data
from validation_agent import validate_claims
from eligibility_agent import eligibility_agent
from policy_agent import policy_agent
from fraud_detection_agent import fraud_agent
from explanation_agent import explanation_agent
from IPython.display import Image, display

"""
This module defines the multi-agent insurance approval workflow using langgraph.   
"""



# Define state schema (make optional with total=False)
class State(TypedDict, total=False):
    claim_id: str
    status: str
    validation_result: dict
    eligibility_result: dict
    policy_response: str
    fraud_result: dict
    explanation: str


def build_graph():
    """Build multi-agent insurance approval workflow with conditional edges."""
    data_store = load_data()

    # Validation Agent Node
    def validation_node(state: State):
        claim_id = state["claim_id"]
        result = validate_claims(claim_id)
        state["validation_result"] = result
        if result["valid"] is False:
            state["status"] = "Rejected - Invalid Data"
            return state
        print("Validation Agent Node done")
        return state

    # Eligibility Agent Node
    def eligibility_node(state: State):
        claim_id = state["claim_id"]
        result = eligibility_agent(claim_id)
        state["eligibility_result"] = result
        if result["eligible"] is False:
            state["status"] = "Denied - Not Eligible"
            return state
        print("Eligibility Agent Node done")
        return state



    # Policy Agent Node (LLM + Vector DB) - supporting evidence
    def policy_agent_node(state: State):
        claim_id = state["claim_id"]

        # Get claim info
        claim_info = data_store["claims"][data_store["claims"]["claim_id"] == claim_id].iloc[0].to_dict()
        patient_info = data_store["patients"][data_store["patients"]["patient_id"] == claim_info["patient_id"]].iloc[0].to_dict()
        plan_id = patient_info.get("plan_id")
        eligibility_result = state.get("eligibility_result", {})

        # Build prompt for policy agent
        decision = eligibility_result if isinstance(eligibility_result, str) else eligibility_result.get("decision", "Unknown")
        prompt = f"""
        Claim ID: {claim_id}
        Plan: {plan_id}
        Procedure: {claim_info['procedure_code']} ({claim_info.get('procedure_name', '')})

        The eligibility agent marked this claim as: {decision}

        Task for you, Policy Agent:
        - Provide supporting excerpts from the policy documents related to this plan and procedure.
        - Include any coverage notes, limitations, and prior authorization requirements.
        - Format the response as a list of key excerpts.
        """

        # Invoke the policy agent LLM
        response = policy_agent(prompt)

        # Store in state
        state["policy_response"] = response
        print(f"Policy Agent Node done for claim {claim_id}")
        return state

 
    # Fraud Detection Agent Node
    def fraud_node(state: State):
        claim_id = state["claim_id"]
        result = fraud_agent(claim_id)
        state["fraud_result"] = result
        if result["fraud_flag"]:
            state["status"] = "Flagged for Fraud"
        else:
            state["status"] = "Approved"
        print("Fraud Detection Agent Node done")
        return state

     # Explanation Agent Node (LLM-generated human-friendly summary)
    def explanation_node(state: State):
        explanation = explanation_agent(state)   # pass whole state as dict
        state["explanation"] = explanation
        return state

    # Build graph
    graph = StateGraph(State)
    graph.add_node("validation_agent", validation_node)
    graph.add_node("eligibility_agent", eligibility_node)
    graph.add_node("policy_agent_node", policy_agent_node)
    graph.add_node("fraud_agent", fraud_node)
    graph.add_node("explanation_agent", explanation_node)

    graph.set_entry_point("validation_agent")
    graph.add_edge("validation_agent", "eligibility_agent")
    graph.add_edge("eligibility_agent", "policy_agent_node")
    graph.add_edge("policy_agent_node", "fraud_agent")
    graph.add_edge("fraud_agent", "explanation_agent")    
    graph.add_edge("explanation_agent", END)
    return graph
