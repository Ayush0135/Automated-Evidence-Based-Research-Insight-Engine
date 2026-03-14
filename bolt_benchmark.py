import time
import sys
from unittest.mock import MagicMock
import types

# Mocking modules before they are imported by stages
mock_llm = types.ModuleType('utils.llm')
mock_llm.query_groq = MagicMock()
sys.modules['utils.llm'] = mock_llm

# Mock search to avoid issues if any stage imports it
sys.modules['utils.search'] = types.ModuleType('utils.search')

from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, json_mode=True, fallback_to_others=True):
    time.sleep(0.5)  # Simulate API latency
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

mock_llm.query_groq.side_effect = mock_query_groq

def run_benchmark():
    num_docs = 6
    docs = [
        {
            "title": f"Doc {i}",
            "analysis": {
                "research_problem": "p",
                "methodology": "m",
                "key_findings": "f",
                "novelty_assessment": "n"
            }
        }
        for i in range(num_docs)
    ]
    topic = "Test Topic"

    print(f"Benchmarking Stage 4 with {num_docs} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"\n--- Benchmark Results ---")
    print(f"Stage 4 took {duration:.2f} seconds.")

    # Check completeness
    if len(results) != num_docs:
        print(f"FAILED: Expected {num_docs} results, got {len(results)}")
        return False

    # Check order
    order_preserved = True
    for i in range(num_docs):
        if results[i]['title'] != f"Doc {i}":
            print(f"FAILED: Order mismatch at index {i}. Expected Doc {i}, got {results[i]['title']}")
            order_preserved = False
            break

    if order_preserved:
        print("PASSED: Document order is preserved.")

    return True

if __name__ == "__main__":
    run_benchmark()
