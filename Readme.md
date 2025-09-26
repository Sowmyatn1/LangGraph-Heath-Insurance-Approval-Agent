Insurance Approval Agent


Welcome to the Insurance Approval Agent repository!
This project demonstrates how to leverage LangGraph for building a smart multi-agent system that automates the insurance claim approval process.


The workflow uses multiple specialized language model (LLM) agents to handle tasks such as:

Validating claims for missing or incorrect data

Checking patient eligibility against insurance plans

Retrieving relevant policy documents and coverage details

Detecting potential fraudulent activity

Generating a clear, human-friendly explanation of the decision

The agent is designed to interact with claims data, invoke necessary tools (like a vector database for policy lookup), and provide a seamless claim approval experience for insurance teams.

Features

Validation Agent – Ensures claims have valid data.

Eligibility Agent – Checks claim eligibility against patient & plan details.

Policy Agent – Uses a vector database + LLM to provide supporting policy excerpts.

Fraud Detection Agent – Flags suspicious claims.

Explanation Agent – Summarizes decisions in simple, human-friendly language.

Streamlit UI – Interactive web interface to test claims and visualize results.

LangGraph Workflow – Orchestrates agents in a stateful graph-based workflow.

📂 Project Structure
Insurance_Approval_Agent/
│── agentUI.py              # Streamlit frontend
│── langgraph_workflow.py   # Core workflow (build_graph)
│── policy_agent.py         # Policy agent (LLM + vector DB)
│── eligibility_agent.py    # Eligibility logic
│── validation_agent.py     # Validation rules
│── fraud_detection_agent.py# Fraud detection logic
│── explanation_agent.py    # Summarizes decision
│── vectordb.py             # Vector database setup (Pinecone/FAISS)
│── data_loader.py          # Loads claims, patients, policies
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation

⚙️ Installation

Clone the repository

git clone https://github.com/your-username/Insurance_Approval_Agent.git
cd Insurance_Approval_Agent


Set up a virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


If you face issues with pyarrow or pandas, install them separately:

pip install pyarrow pandas

▶️ Running the Project
1. Run workflow from CLI
python -m langgraph_workflow


This runs the multi-agent workflow on a test claim (C20003) and prints the final decision.

2. Run Streamlit UI
streamlit run agentUI.py


Open http://localhost:8501
 in your browser.

📊 Workflow Overview

The claim approval flow works as follows:

[Validation Agent] → [Eligibility Agent] → [Policy Agent] → [Fraud Detection Agent] → [Explanation Agent] → END


Invalid claims → Rejected

Not eligible → Denied

Fraud detected → Flagged

Otherwise → Approved with explanation

🔧 Configuration

Vector DB: Currently supports Pinecone via vectordb.py.

LLM: Configured inside policy_agent.py and explanation_agent.py.

Data: Claims & patient data loaded from data_loader.py.

Make sure to set your API keys (e.g., OpenAI, Pinecone) in environment variables:

export OPENAI_API_KEY="your-key"
export PINECONE_API_KEY="your-key"

📌 Requirements

Python 3.12+

Streamlit

LangChain

LangGraph

Pinecone or FAISS for vector storage

🛠 Future Enhancements

Add audit logging of claim decisions

Add explainability dashboard in Streamlit

Integrate with real FHIR/EHR datasets

Support for multiple vector DB backends
