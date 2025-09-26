"""
This Agent access the vector databse that we created in src/vectordb and checks the policy docs 
"""
from langchain.chat_models import init_chat_model
from vectordb import query_vectorstore, create_vectorstore


#this the policy agent created using Gemini
# Make sure Pinecone is ingested
create_vectorstore()

# STEP 1: Initialize Gemini LLM
llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.5
)

# STEP 2: Define a wrapper for policy queries
def policy_agent(query: str):
    # 1. Get top 3 relevant chunks from Pinecone
    docs = query_vectorstore(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # 2. Prepare prompt for LLM
    prompt = f"Answer the question based on the following policy documents:\n{context}\n\nQuestion: {query}\nAnswer:"

    # 3. Generate answer using Gemini
    response = llm.invoke(prompt)
    return response.content

# Test
if __name__ == "__main__":
    query = "Does MedicareC cover MRI Brain?"
    print("Policy Agent Response:", policy_agent(query))
