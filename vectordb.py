# src/vectordb.py
"""
this file will read all the txt files under the path data/policyDocs MedicareA_policy.txt,MedicareB_policy.txt.MedicareC_policy.txt
we are using Pinecone Vector DB to chunk and load all the polcy docs under one index which is index_name="insurance-policies"
"""
import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()

# 1. Initialize Pinecone
def init_pinecone(index_name="insurance-policies"):
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("Set the PINECONE_API_KEY environment variable.")

    pc = Pinecone(api_key=api_key)

    # Check if index exists, else create
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # must match embedding model dimensions
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    return pc, index_name

# 2. Load and split documents
def load_policy_docs(path="data/policyDocs/"):
    loader = DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(docs)

# 3. Create Pinecone vectorstore
def create_vectorstore(index_name="insurance-policies"):
    pc, index_name = init_pinecone(index_name)

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    docs = load_policy_docs()
    vectorstore = PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name=index_name
    )
    return vectorstore

# 4. Query helper
def query_vectorstore(query, index_name="insurance-policies", k=3):
    pc, index_name = init_pinecone(index_name)

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    return vectorstore.similarity_search(query, k=k)


if __name__ == "__main__":
    # Run once to ingest all policy docs
    print("Ingesting documents into Pinecone...")
    create_vectorstore()
    print("Done ✅")
