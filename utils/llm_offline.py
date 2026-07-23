import os
import ollama
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

# Configuration for Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
# Default to localhost if not set, typical for local runs.
# Only use https://ollama.com/api if actually intended (which requires keys usually).
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

_client_cached = False
_client = None

def get_client():
    """
    Returns a cached Ollama Client instance if OLLAMA_API_KEY is present,
    preventing repeated Client object instantiation.
    """
    global _client_cached, _client
    if not _client_cached:
        if OLLAMA_API_KEY:
            # If we have an API key, we use the Client with headers
            _client = Client(
                host=OLLAMA_HOST,
                headers={
                    'Authorization': f'Bearer {OLLAMA_API_KEY}'
                }
            )
        _client_cached = True
    return _client

def query_offline_llm(prompt, model_name=None):
    """
    Queries Ollama (Cloud if API Key present, else local).
    """
    client = get_client()
    target_model = model_name if model_name else OLLAMA_MODEL
    
    try:
        messages = [
            {'role': 'system', 'content': 'You are a helpful research assistant.'},
            {'role': 'user', 'content': prompt}
        ]
        
        if client:
            response = client.chat(model=target_model, messages=messages)
        else:
            response = ollama.chat(model=target_model, messages=messages)
            
        return response['message']['content']
    except Exception as e:
        error_str = str(e).lower()
        if "not found" in error_str:
            return f"Error: Ollama model '{OLLAMA_MODEL}' not found."
        if "401" in error_str or "unauthorized" in error_str:
            return "Error: Ollama Cloud API Key is invalid or unauthorized."
        print(f"Error querying Ollama: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test Ollama
    mode = "Cloud" if OLLAMA_API_KEY else "Local"
    print(f"Testing Ollama ({mode}) with model: {OLLAMA_MODEL}")
    test_response = query_offline_llm("Say hello!")
    print(f"Response: {test_response}")
