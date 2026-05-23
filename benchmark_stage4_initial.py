
import time
import sys
from unittest.mock import patch, MagicMock

# Mock dependencies that might not be installed or need API keys
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, json_mode=False, fallback_to_others=True):
    # Simulate LLM processing time
    time.sleep(1)
    return '{"score": 8, "strengths": "Good methodology", "weaknesses": "None"}'

def run_benchmark():
    topic = "AI Performance Optimization"
    documents = [
        {"title": f"Paper {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
        for i in range(5)
    ]

    print(f"Benchmarking Stage 4 with {len(documents)} documents and 3 workers...")
    print("Each mock LLM call takes 1 second.")

    start_time = time.time()
    with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
        results = stage4_academic_scoring(documents, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"\nTotal duration: {duration:.2f} seconds")

    # Expected: 5 docs, 3 workers, 1s each.
    # Round 1: Docs 0, 1, 2 (1s)
    # Round 2: Docs 3, 4 (1s)
    # Total: ~2s

    if duration < 3.0:
        print("SUCCESS: Parallelization confirmed (took less than 3 seconds for 5 documents).")
    else:
        print("FAILURE: Execution took too long, parallelization might not be working as expected.")

    if len(results) == 5:
        print("SUCCESS: All documents scored.")
    else:
        print(f"FAILURE: Only {len(results)} documents scored.")

if __name__ == "__main__":
    run_benchmark()
