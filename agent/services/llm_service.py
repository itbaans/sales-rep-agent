import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Initializes and returns the LLM client."""
    llm = ChatOpenAI(
        model="gpt-4o", 
        temperature=0, 
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return llm