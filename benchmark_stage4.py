import time
import sys
from unittest.mock import MagicMock
import json

# Mock dependencies BEFORE importing any module that uses them
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

import stages.stage4_scoring as stage4

def benchmark_stage4_parallel():
    # Mock query_groq to simulate network delay
    def mock_query_groq(prompt, **kwargs):
        time.sleep(0.5)  # Simulate 500ms delay
        return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

    # Overwrite the imported function in the module
    stage4.query_groq = mock_query_groq

    test_docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
        for i in range(10)
    ]
    topic = "Test Topic"

    print(f"Benchmarking Parallel Stage 4 with 10 documents and 3 workers...")
    start_time = time.time()
    results = stage4.stage4_academic_scoring(test_docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 (Parallel) took {duration:.2f} seconds.")
    print(f"Results count: {len(results)}")

    # Analysis:
    # Sequential: 10 docs * 0.5s = 5.0s
    # Parallel (3 workers): 10 / 3 batches = 4 rounds * 0.5s = 2.0s
    # Speedup: ~2.5x

    return duration

if __name__ == "__main__":
    benchmark_stage4_parallel()
