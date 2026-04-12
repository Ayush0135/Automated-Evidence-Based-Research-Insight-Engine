import sys
import time
import json
from unittest.mock import MagicMock

# Mock dependencies BEFORE importing the stage
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.llm_offline'] = MagicMock()
sys.modules['utils.search'] = MagicMock()

# Now import the stage
from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)  # Simulate API latency
    return json.dumps({"score": 8, "strengths": "Strong", "weaknesses": "None"})

mock_llm.query_groq.side_effect = mock_query_groq

def run_benchmark():
    docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
        for i in range(6)
    ]
    topic = "Test Topic"

    print(f"Starting benchmark with {len(docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Benchmark finished in {duration:.2f} seconds.")

    # Check order
    order_correct = True
    for i, res in enumerate(results):
        if res['title'] != f"Doc {i}":
            print(f"ORDER MISMATCH: Expected Doc {i}, got {res['title']}")
            order_correct = False
            break

    if order_correct:
        print("Order preserved successfully.")

    return duration

if __name__ == "__main__":
    run_benchmark()
