import os
from dotenv import load_dotenv
from agent.services.llm_service import get_llm

load_dotenv()

def test_langsmith_integration():
    """Test if LangSmith tracing is working"""
    print("Testing LangSmith integration...")
    
    # Check environment variables
    required_vars = ['LANGCHAIN_TRACING_V2', 'LANGCHAIN_API_KEY', 'LANGCHAIN_PROJECT']
    for var in required_vars:
        if not os.getenv(var):
            print(f"❌ Missing environment variable: {var}")
            return False
        else:
            print(f"✅ {var} is set")
    
    # Test LLM with tracing
    try:
        llm = get_llm()
        response = llm.invoke("Hello, this is a test message for LangSmith tracing.")
        print(f"✅ LLM response: {response.content[:50]}...")
        print("✅ Check your LangSmith dashboard for traces!")
        return True
    except Exception as e:
        print(f"❌ Error testing LLM: {e}")
        return False

if __name__ == "__main__":
    test_langsmith_integration()