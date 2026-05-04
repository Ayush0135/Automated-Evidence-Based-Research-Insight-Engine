
import sys
import time
import json
from unittest.mock import MagicMock, patch

# Mock dependencies to avoid import errors
# We need to mock 'google', 'google.generativeai', etc.
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['termcolor'] = MagicMock()

import stages.stage4_scoring as stage4

def mock_query_groq(prompt, json_mode=False, fallback_to_others=True):
    time.sleep(0.5)
    return json.dumps({
        "score": 8,
        "strengths": "Good methodology",
        "weaknesses": "None"
    })

def run_benchmark():
    test_docs = []
    for i in range(10):
        test_docs.append({
            "title": f"Doc {i}",
            "analysis": {
                "research_problem": "Problem X",
                "methodology": "Method Y",
                "key_findings": "Findings Z",
                "novelty_assessment": "High"
            }
        })

    topic = "Test Topic"

    print(f"Running benchmark with {len(test_docs)} documents...")

    with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
        start_time = time.time()
        results = stage4.stage4_academic_scoring(test_docs, topic)
        end_time = time.time()

    duration = end_time - start_time
    print(f"Total time: {duration:.2f} seconds")

    # Verify order
    order_preserved = True
    for i, doc in enumerate(results):
        if doc['title'] != f"Doc {i}":
            order_preserved = False
            print(f"ORDER MISMATCH: Expected Doc {i}, got {doc['title']}")
            break

    if order_preserved:
        print("Order preserved: YES")
    else:
        print("Order preserved: NO")

    return duration, order_preserved

if __name__ == "__main__":
    run_benchmark()
