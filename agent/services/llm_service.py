import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm():
    """Initializes and returns the Gemini LLM client."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",  # You can also use "gemini-1.5-pro" if needed
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    return llm
