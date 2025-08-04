def chunk_pdf_doc(pdf_path: str) -> list[Document]:
    
    # Extract text from PDF
    pdf_reader = PdfReader(pdf_path)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() if page.extract_text() else ""

    # Create a Document with the extracted text
    pdf_doc = Document(page_content=pdf_text, metadata={"source": pdf_path})

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_documents([pdf_doc])

def make_dense_emb_model(chunks: list[Document], google_api_key: str):
    """
    Creates a dense embedding model and a retriever from document chunks.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 5})

# --- 3. BM25 Retriever ---
def make_bm25_index(chunks: list[Document]):
    """
    Creates a BM25 index from document chunks.
    """
    return BM25Retriever.from_documents(chunks)

# import os
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.retrievers import BM25Retriever, EnsembleRetriever
# from langchain.schema import Document
# from typing import List
# from PyPDF2 import PdfReader

# # --- 1. Chunking Documents ---
# def chunk_pdf_doc(pdf_path: str) -> list[Document]:
#     """
#     Chunks a single PDF document using a recursive strategy.

#     Args:
#         pdf_path (str): Path to the PDF file.

#     Returns:
#         list[Document]: A list of chunked documents.
#     """
#     # Extract text from PDF
#     pdf_reader = PdfReader(pdf_path)
#     pdf_text = ""
#     for page in pdf_reader.pages:
#         pdf_text += page.extract_text() if page.extract_text() else ""

#     # Create a Document with the extracted text
#     pdf_doc = Document(page_content=pdf_text, metadata={"source": pdf_path})

#     # Split the document into chunks
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len,
#         is_separator_regex=False,
#     )

#     return text_splitter.split_documents([pdf_doc])

# # --- 2. Dense Embeddings and Retriever ---
# def make_dense_emb_model(chunks: list[Document], google_api_key: str):
#     """
#     Creates a dense embedding model and a retriever from document chunks.
#     """
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
#     vectorstore = FAISS.from_documents(chunks, embeddings)
#     return vectorstore.as_retriever(search_kwargs={"k": 5})

# # --- 3. BM25 Retriever ---
# def make_bm25_index(chunks: list[Document]):
#     """
#     Creates a BM25 index from document chunks.
#     """
#     return BM25Retriever.from_documents(chunks)


# def main():
#     # Set your Google API Key
#     # Make sure to set your GOOGLE_API_KEY environment variable
#     google_api_key = "AIzaSyDMw9YHPKhxl0jAPCYwJhujdGgpdiry_JA"

#     if not google_api_key:
#         raise ValueError("GOOGLE_API_KEY environment variable not set.")

#     # Example documents
#     pdf_doc = "Systems Limited Policies.pdf"

#     # 1. Chunk the documents
#     chunks = chunk_pdf_doc(pdf_doc)

#     # 2. Create the dense retriever
#     dense_retriever = make_dense_emb_model(chunks, google_api_key)

#     # 3. Create the BM25 retriever
#     bm25_retriever = make_bm25_index(chunks)
#     bm25_retriever.k = 2

#     # --- 4. Fuse Search Results with EnsembleRetriever ---
#     ensemble_retriever = EnsembleRetriever(
#         retrievers=[dense_retriever, bm25_retriever],
#         weights=[0.1, 0.9]
#     )

#     # --- 5. Retrieve Documents ---
#     question = "employee"
#     retrieved_docs = ensemble_retriever.invoke(question)

#     print("--- Retrieved Documents ---")
#     for doc in retrieved_docs:
#         print(doc.page_content)

# # --- Main Execution ---
# if __name__ == '__main__':
#     main()