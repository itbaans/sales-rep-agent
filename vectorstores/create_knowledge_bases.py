import json
import os
import pickle
import re
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


JSON_RETRIEVARS = {
    "company_profile": ["vectorstores/json_files_indexes/company_profile_faiss_index", "vectorstores/json_files_indexes/company_profile_bm25_index.pkl"],
    "company_price_models": ["vectorstores/json_files_indexes/company_price_models_faiss_index", "vectorstores/json_files_indexes/company_price_models_bm25_index.pkl"],
    "company_technical": ["vectorstores/json_files_indexes/company_technical_faiss_index", "vectorstores/json_files_indexes/company_technical_bm25_index.pkl"],
    "company_projects": ["vectorstores/json_files_indexes/company_projects_faiss_index", "vectorstores/json_files_indexes/company_projects_bm25_index.pkl"],
}

JSON_FILES = {
   "company_profile": "data/company_docs/company_profile.json",
   "company_price_models": "data/company_docs/company_price_models.json",
   "company_technical": "data/company_docs/company_technical.json",
   "company_projects": "data/company_docs/projects.json"
}

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

def chunk_txt_doc(txt_path: str) -> List[Document]:
    # Read the whole text file
    with open(txt_path, "r", encoding="utf-8") as f:
        txt_content = f.read()

    # Remove metadata block if it exists
    cleaned_text = re.sub(
        r"=== METADATA ===\s*\{.*?\}\s*", 
        "", 
        txt_content, 
        flags=re.DOTALL
    )

    # Wrap into a Document object
    doc = Document(page_content=cleaned_text.strip(), metadata={"source": txt_path})

    # Use the same splitter configuration
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
    return vectorstore.as_retriever(search_kwargs={"k": 2})

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
    return vectorstore.as_retriever(search_kwargs={"k": 2})

# --- 5. Load BM25 Retriever ---
def load_bm25_index(load_path: str):
    with open(load_path, "rb") as f:
        return pickle.load(f)


def extract_json_keypaths(json_data, parent_key=""):
    keypaths = []

    if isinstance(json_data, dict):
        for k, v in json_data.items():
            full_key = f"{parent_key}->{k}" if parent_key else k
            keypaths.append(full_key)
            keypaths.extend(extract_json_keypaths(v, full_key))
    elif isinstance(json_data, list):
        for item in json_data:
            keypaths.extend(extract_json_keypaths(item, parent_key))
    return keypaths

def chunk_json_keys(json_path: str) -> List[Document]:
    import json

    with open(json_path, "r") as f:
        data = json.load(f)

    keypaths = extract_json_keypaths(data)
    docs = [Document(page_content=kp, metadata={"key": kp}) for kp in keypaths]
    return docs


def get_value_by_keypath(data, chain):
    keys = chain.split("->")
    current = data
    for key in keys:
        if isinstance(current, list):
            current = [item.get(key) for item in current if isinstance(item, dict)]
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current

# --- 6. Initialize Indexes ---
def initialize_vector_knowledge():
    global dense_retriever, bm25_retriever

    docs_dir = os.getenv("COMPANY_DOCS_DIR", "data/company_docs")

    faiss_path = os.getenv("FAISS_PATH", "vectorstores/faiss_index")
    bm25_path = os.getenv("BM25_PATH", "vectorstores/bm25_index.pkl")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    # Folders we care about
    target_folders = ["capability_docs", "generated_docs", "pricing_docs", "project_docs"]

    if not os.path.exists(faiss_path) or not os.path.exists(bm25_path):
        print("Processing TXT files and creating indexes...")

        txt_paths = []
        for folder in target_folders:
            folder_path = os.path.join(docs_dir, folder)
            if os.path.exists(folder_path):
                for f in os.listdir(folder_path):
                    if f.endswith(".txt"):
                        txt_paths.append(os.path.join(folder_path, f))

        if not txt_paths:
            raise FileNotFoundError("No TXT files found in the specified directories.")

        chunks = []
        for txt_path in txt_paths:
            print(f"Processing {txt_path}...")
            chunks.extend(chunk_txt_doc(txt_path))  # <-- You'll need a text chunker

        dense_retriever = create_faiss_index(chunks, google_api_key, faiss_path)
        bm25_retriever = create_bm25_index(chunks, bm25_path)

    else:
        print("Loading saved indexes...")

        dense_retriever = load_faiss_index(google_api_key, faiss_path)
        bm25_retriever = load_bm25_index(bm25_path)

def initialize_json_knowledge():

    for json_name, (faiss_path, bm25_path) in JSON_RETRIEVARS.items():
        if not os.path.exists(faiss_path) or not os.path.exists(bm25_path):
            print(f"Processing JSON for {json_name} and creating indexes...")
            json_path = JSON_FILES[json_name]
            chunks = chunk_json_keys(json_path)
            google_api_key = os.getenv("GOOGLE_API_KEY")
            create_faiss_index(chunks, google_api_key, faiss_path)
            create_bm25_index(chunks, bm25_path)

def search_json_keys_and_return_values(query: str, top_k: int = 10, type: str = "company_profile") -> str:
    # Set top_k on both retrievers
    
    if type not in JSON_RETRIEVARS:
        raise ValueError(f"Invalid type: {type}. Must be one of {list(JSON_RETRIEVARS.keys())}.")
    
    faiss_path, bm25_path = JSON_RETRIEVARS[type]

    # Load original JSON data
    json_path = JSON_FILES[type]
    with open(json_path, "r") as f:
        original_json_data = json.load(f)

    json_dense_retriever = load_faiss_index(os.getenv("GOOGLE_API_KEY"), faiss_path)
    json_bm25_retriever = load_bm25_index(bm25_path)

    # Set top_k for BM25 retriever
    json_bm25_retriever.k = top_k

    # Create dense retriever with top_k
    json_dense_retriever.search_kwargs["k"] = top_k

    # Combine them
    ensemble = EnsembleRetriever(
        retrievers=[json_dense_retriever, json_bm25_retriever],
        weights=[0.5, 0.5]
    )

    # Get matching key paths
    retrieved_docs: List[Document] = ensemble.invoke(query)
    retrieved_keys = [doc.page_content.strip() for doc in retrieved_docs][:top_k]
    #print(retrieved_keys)

    # Lookup values
    results = []
    for key in retrieved_keys:
        value = get_value_by_keypath(original_json_data, key)
        if value is not None:
            results.append(f"{key} -> {value}")

    #print(results)

    if not results:
        return "No relevant data found."
    
    return "\n".join(results)


# --- 7. Query Interface ---
def search_knowledge_base_rag(question: str) -> str:
    # Set number of BM25 results
    bm25_retriever.k = 2

    # Create ensemble retriever
    ensemble = EnsembleRetriever(
        retrievers=[dense_retriever, bm25_retriever],
        weights=[0.5, 0.5]
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
        f"Carefully read the documents and extract the most relevant information that answers the query. "
        f"Use exact details, facts, numbers, or entities from the documents whenever possible. "
        f"If multiple documents provide partial answers, combine them into a single, coherent response. "
        f"Do not add information that is not explicitly present in the documents. "
        f"If the documents do not contain enough information to answer, respond with: "
        f"'Information not found in the provided documents.'"
    )

    # Run through LLM
    llm = get_llm()
    response = llm.invoke(prompt).content

    # Return text response
    return response

# --- Optional Main Entry Point ---
if __name__ == "__main__":
    initialize_json_knowledge()
    results = search_json_keys_and_return_values("projects")
    print("--- Retrieved Documents ---")
    print(results)
