
import time
import sys
from unittest.mock import MagicMock, patch

# Mock the modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)  # Simulate API latency
    return '{"score": 8, "strengths": "Good paper", "weaknesses": "None"}'

def run_benchmark():
    mock_llm.query_groq.side_effect = mock_query_groq

    test_docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]

    print(f"Running Stage 4 benchmark with {len(test_docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(test_docs, "Test Topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 completed in {duration:.2f} seconds.")

    # Verify order preservation
    titles = [doc['title'] for doc in results]
    expected_titles = [f"Doc {i}" for i in range(6)]

    if titles == expected_titles:
        print("✅ Document order preserved.")
    else:
        print("❌ Document order SCRAMBLED!")
        print(f"Actual: {titles}")
        print(f"Expected: {expected_titles}")

if __name__ == "__main__":
    run_benchmark()
