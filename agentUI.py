# agentUI.py
"""
This is a frontend UI for the Insurance Approval Agent.input will be the claim ID and invokes the langgraph workflow
"""
import streamlit as st
from langgraph_workflow import build_graph

# Build the workflow graph once
workflow_graph = build_graph()
workflow = workflow_graph.compile()

# Set page configuration
st.set_page_config(page_title="Insurance Approval Agent", layout="wide")

# Main content
st.title("🏥 Insurance Approval Agent")
st.write("Submit a Claim ID to run through the multi-agent workflow (Validation → Eligibility → Policy → Fraud → Explanation).")

# Sidebar
st.sidebar.header("⚙️ Settings")
test_claim_id = st.sidebar.text_input("Enter Claim ID", value="C20003")

if st.sidebar.button("Run Workflow"):
    with st.spinner("Processing claim through all agents..."):
        initial_state = {"claim_id": test_claim_id}
        result = workflow.invoke(initial_state)

    # Final Results
    st.success("✅ Workflow completed")

    st.subheader("📌 Final Decision")
    st.write(f"**Status:** {result.get('status', 'Unknown')}")

    st.subheader("📝 Human Explanation")
    st.write(result.get("explanation", "No explanation available."))

    # Expanders for details
    with st.expander("🔍 Validation Result"):
        st.json(result.get("validation_result", {}))

    with st.expander("🧾 Eligibility Result"):
        st.json(result.get("eligibility_result", {}))

    with st.expander("📑 Policy Evidence"):
        st.write(result.get("policy_response", "No policy response"))

    with st.expander("🚨 Fraud Detection Result"):
        st.json(result.get("fraud_result", {}))

else:
    st.info("👈 Enter a Claim ID and click **Run Workflow** to begin.")
