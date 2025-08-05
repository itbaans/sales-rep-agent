import os
import pickle
from typing import List
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from agent.services.llm_service import get_llm

# Load environment variables
load_dotenv()

# Global retrievers
dense_retriever = None
bm25_retriever = None

# --- 1. Chunking Documents ---
def chunk_pdf_doc(pdf_path: str) -> List[Document]:
    pdf_reader = PdfReader(pdf_path)
    pdf_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
    doc = Document(page_content=pdf_text, metadata={"source": pdf_path})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents([doc])

# --- 2. Create and Save FAISS Retriever ---
def create_faiss_index(chunks: List[Document], api_key: str, save_path: str):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(save_path)
    return vectorstore.as_retriever(search_kwargs={"k": 5})

# --- 3. Create and Save BM25 Retriever ---
def create_bm25_index(chunks: List[Document], save_path: str):
    retriever = BM25Retriever.from_documents(chunks)
    with open(save_path, "wb") as f:
        pickle.dump(retriever, f)
    return retriever

# --- 4. Load FAISS Retriever ---
def load_faiss_index(api_key: str, load_path: str):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    vectorstore = FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 5})

# --- 5. Load BM25 Retriever ---
def load_bm25_index(load_path: str):
    with open(load_path, "rb") as f:
        return pickle.load(f)

# --- 6. Initialize Indexes ---
def initialize_vector_knowledge():
    global dense_retriever, bm25_retriever

    pdf_path = os.getenv("PDF_PATH", "example.pdf")
    faiss_path = os.getenv("FAISS_PATH", "vectorstores/faiss_index")
    bm25_path = os.getenv("BM25_PATH", "vectorstores/bm25_index.pkl")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not os.path.exists(faiss_path) or not os.path.exists(bm25_path):
        print("Processing PDF and creating indexes...")

        chunks = chunk_pdf_doc(pdf_path)

        dense_retriever = create_faiss_index(chunks, google_api_key, faiss_path)
        bm25_retriever = create_bm25_index(chunks, bm25_path)
    else:
        print("Loading saved indexes...")

        dense_retriever = load_faiss_index(google_api_key, faiss_path)
        bm25_retriever = load_bm25_index(bm25_path)

# --- 7. Query Interface ---
def search_knowledge_base(question: str) -> str:
    # Set number of BM25 results
    bm25_retriever.k = 2

    # Create ensemble retriever
    ensemble = EnsembleRetriever(
        retrievers=[dense_retriever, bm25_retriever],
        weights=[0.1, 0.9]
    )

    # Run retrieval
    retrieved_docs: List[Document] = ensemble.invoke(question)

    # Extract and clean contents
    cleaned_contents = [
        f"Doc {i+1}:\n{doc.page_content.strip()}"
        for i, doc in enumerate(retrieved_docs)
        if doc.page_content.strip()
    ]
    joined_docs = "\n\n".join(cleaned_contents)

    # Build prompt
    prompt = (
    f"You are given the following documents retrieved for the query.\n\n"
    f"Query: {question}\n\n"
    f"Documents:\n{joined_docs}\n\n"
    f"Answer the query using only the information from the documents. If the documents do not contain enough information to answer, respond with 'Information not found in the provided documents.'"
    )

    # Run through LLM
    llm = get_llm()
    response = llm.invoke(prompt).content

    # Return text response
    return response

# --- Optional Main Entry Point ---
# if __name__ == "__main__":
#     initialize_vector_knowledge()
#     results = search_knowledge_base("employee")
#     print("--- Retrieved Documents ---")
#     print(results)
