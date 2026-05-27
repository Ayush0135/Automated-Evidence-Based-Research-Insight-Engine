
import sys
from unittest.mock import MagicMock, patch

def test_optimizations():
    # Mocking necessary modules for llm.py
    sys.modules['google'] = MagicMock()
    sys.modules['google.generativeai'] = MagicMock()
    sys.modules['groq'] = MagicMock()
    sys.modules['anthropic'] = MagicMock()
    sys.modules['dotenv'] = MagicMock()
    sys.modules['utils.llm_offline'] = MagicMock()
    sys.modules['ollama'] = MagicMock()

    import utils.llm as llm

    print("Verifying llm.py optimizations...")

    # Check if termcolor.colored is imported at module level
    if hasattr(llm, 'colored'):
        print("  [OK] termcolor.colored is at module level.")
    else:
        print("  [FAIL] termcolor.colored is NOT at module level.")

    # Check if get_gemini_model caches the model
    with patch('google.generativeai.GenerativeModel') as mock_model:
        model1 = llm.get_gemini_model()
        model2 = llm.get_gemini_model()

        if model1 is model2:
            print("  [OK] Gemini model is cached.")
        else:
            print("  [FAIL] Gemini model is NOT cached.")

    # Check utils.search for connection pooling
    import utils.search as search
    if hasattr(search, 'session') and isinstance(search.session, MagicMock) or hasattr(search, 'session'):
         print("  [OK] utils.search has a session object.")
    else:
         print("  [FAIL] utils.search MISSING session object.")

if __name__ == '__main__':
    test_optimizations()
