import sys
from unittest.mock import MagicMock, patch

# Robust mocking to avoid import errors in restricted environment
mock_modules = [
    'google', 'google.genai', 'google.genai.errors',
    'groq', 'anthropic', 'termcolor', 'dotenv', 'ollama'
]
for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

# Now we can import our stage
import stages.stage3_analysis as stage3

def test_optimization():
    print("Testing Stage 3 Optimization...")

    # Create a document with 100,000 characters
    # (Greater than old 64k threshold, but less than new 128k threshold)
    large_text = "Data " * 20000
    print(f"Document length: {len(large_text)} characters")

    doc = {
        "title": "Large Research Paper",
        "raw_text": large_text
    }

    # Mock query_gemini to track calls
    with patch('stages.stage3_analysis.query_gemini') as mock_query:
        # Mocking return value for JSON extraction
        mock_query.return_value = '{"research_problem": "Optimizing LLM pipelines", "methodology": "Increasing context threshold", "key_findings": "Fewer API calls", "limitations": "None", "research_gaps": "N/A", "novelty_assessment": "High", "technical_depth_score": 10, "missing_entities": "None"}'

        result = stage3.analyze_single_document(doc)

        # In the optimized version, it should be exactly 1 call (the final analysis)
        # In the old version, it would have been multiple calls (chunking + final)
        call_count = mock_query.call_count
        print(f"Total LLM calls: {call_count}")

        if call_count == 1:
            print("SUCCESS: Document processed in a single LLM call.")
        else:
            print(f"FAILURE: Document processed in {call_count} calls. Optimization might be missing.")
            sys.exit(1)

if __name__ == "__main__":
    test_optimization()
