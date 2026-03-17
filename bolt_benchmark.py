
import time
import sys
import os
from unittest.mock import MagicMock, patch

# Mock the LLM and search utilities before importing stages
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    print("Benchmarking Stage 4 (Sequential Baseline)...")

    # Mock query_groq to simulate 0.5s latency
    def mock_query_groq(prompt, json_mode=False, fallback_to_others=True):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "Good paper", "weaknesses": "None"}'

    mock_llm.query_groq.side_effect = mock_query_groq

    mock_docs = [
        {"title": f"Paper {i}", "url": f"http://test.com/{i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]

    start_time = time.time()
    results = stage4_academic_scoring(mock_docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"\nTotal Time: {duration:.2f}s")

    # Verify order
    for i, doc in enumerate(results):
        if doc['title'] != f"Paper {i}":
            print(f"ORDER ERROR: Expected Paper {i}, got {doc['title']}")
            return False

    print("Order verified: Success")
    return duration

if __name__ == "__main__":
    benchmark_stage4()
