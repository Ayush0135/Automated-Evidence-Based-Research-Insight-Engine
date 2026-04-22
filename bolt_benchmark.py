
import time
import sys
from unittest.mock import MagicMock, patch

# Mock dependencies before importing the stage
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    print("Benchmarking Stage 4 (Sequential)...")

    # Mock documents
    docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(10)
    ]

    # Mock LLM response with 0.5s delay
    def mock_query(*args, **kwargs):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "S", "weaknesses": "W"}'

    mock_llm.query_groq.side_effect = mock_query

    start_time = time.time()
    results = stage4_academic_scoring(docs, "Topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Total duration: {duration:.2f}s")
    print(f"Results count: {len(results)}")

    # Verify order
    for i, res in enumerate(results):
        if res['title'] != f"Doc {i}":
            print(f"ORDER MISMATCH at {i}: expected Doc {i}, got {res['title']}")
            return
    print("Order preserved.")

if __name__ == "__main__":
    benchmark_stage4()
