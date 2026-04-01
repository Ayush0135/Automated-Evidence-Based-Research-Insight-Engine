import sys
import os
import time
import json
from unittest.mock import MagicMock

# Mock internal modules before importing stages
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = MagicMock()

# Manually set the side effect for query_groq BEFORE importing stage4_scoring
def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)
    # Extract paper title from prompt to return correct mock score
    for i in range(6):
        if f"Document Title: Paper {i}" in prompt:
            return json.dumps({
                "score": 8,
                "strengths": f"Strong Paper {i}",
                "weaknesses": "None"
            })
    return json.dumps({"score": 0})

mock_llm.query_groq.side_effect = mock_query_groq

from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_parallel_scoring():
    print("\n--- BENCHMARKING STAGE 4 PARALLEL SCORING ---")

    # Setup Mock Data
    topic = "Quantum Computing Impacts on Cryptography"
    mock_docs = []
    for i in range(6):
        mock_docs.append({
            "title": f"Paper {i}",
            "analysis": {
                "research_problem": f"Problem {i}",
                "methodology": f"Method {i}",
                "key_findings": f"Findings {i}",
                "novelty_assessment": f"Novelty {i}"
            }
        })

    # 1. Measure Execution Time
    start_time = time.time()
    results = stage4_academic_scoring(mock_docs, topic)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"\nTotal Time for 6 docs (Parallel): {total_time:.2f}s")

    # 2. Verify Order Preservation
    print("\nVerifying Order Preservation...")
    if not results:
        print("FAILURE: No results returned.")
        sys.exit(1)

    all_ordered = True
    for idx, doc in enumerate(results):
        expected_title = f"Paper {idx}"
        if doc['title'] != expected_title:
            print(f"  [Error] Order mismatch at index {idx}: Expected {expected_title}, got {doc['title']}")
            all_ordered = False
        else:
            print(f"  [OK] {doc['title']} is in the correct position.")

    if all_ordered:
        print("\nSUCCESS: Stage 4 Parallelization preserves order.")
    else:
        print("\nFAILURE: Stage 4 Parallelization scrambled order.")
        sys.exit(1)

    # 3. Verify Speedup
    # Sequential would be 6 * 0.5s = 3.0s
    # Parallel (3 workers) should be ~ 2 * 0.5s = 1.0s (+ overhead)
    # Threshold < 2.0s is safe for a 3.0s sequential baseline
    if total_time < 2.0:
        print(f"SUCCESS: Significant speedup detected ({total_time:.2f}s vs expected 3.00s sequential).")
    else:
        print(f"FAILURE: Performance gain not significant ({total_time:.2f}s).")
        sys.exit(1)

if __name__ == "__main__":
    test_stage4_parallel_scoring()
