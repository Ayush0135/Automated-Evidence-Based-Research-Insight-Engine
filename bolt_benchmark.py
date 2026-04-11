import time
import sys
from unittest.mock import MagicMock

def mock_query_groq(prompt, json_mode=False, fallback_to_others=True):
    time.sleep(0.5)
    return '{"score": 8, "strengths": "Good methodology", "weaknesses": "None"}'

# Create a mock for utils.llm
mock_llm = MagicMock()
mock_llm.query_groq = mock_query_groq

# Patch sys.modules
sys.modules['utils.llm'] = mock_llm

import stages.stage4_scoring as stage4

def main():
    docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
        for i in range(6)
    ]
    topic = "Quantum Computing"

    start_time = time.time()
    results = stage4.stage4_academic_scoring(docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"\nExecution Time: {duration:.2f} seconds")
    print(f"Results count: {len(results)}")

    # Verify order
    order_preserved = True
    for i, res in enumerate(results):
        if res['title'] != f"Doc {i}":
            print(f"Order Mismatch: Expected Doc {i}, got {res['title']}")
            order_preserved = False

    if order_preserved:
        print("Order preserved successfully.")

if __name__ == "__main__":
    main()
