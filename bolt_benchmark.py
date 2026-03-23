
import time
import sys
from unittest.mock import MagicMock, patch

# Mock the LLM and search modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)  # Simulate API latency
    return '{"score": 8, "strengths": "Good paper", "weaknesses": "None"}'

mock_llm.query_groq.side_effect = mock_query_groq

def benchmark_stage4():
    test_docs = [
        {"title": f"Paper {i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]
    topic = "Test Topic"

    print(f"Benchmarking Stage 4 with {len(test_docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(test_docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 took {duration:.2f} seconds.")

    # Verify order
    for i, doc in enumerate(results):
        if doc['title'] != f"Paper {i}":
            print(f"ORDER MISMATCH: Expected Paper {i}, got {doc['title']}")
            return False

    print("Order verified.")
    return duration

if __name__ == "__main__":
    benchmark_stage4()
