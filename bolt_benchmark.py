
import sys
import time
from unittest.mock import MagicMock

# Mock the LLM call before importing the stage
mock_llm = MagicMock()
mock_utils_llm = MagicMock()
mock_utils_llm.query_groq = mock_llm
sys.modules['utils.llm'] = mock_utils_llm

# Mock utils.search as well just in case
sys.modules['utils.search'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    # Setup mock data
    topic = "Quantum Computing"
    analyzed_docs = [
        {
            "title": f"Paper {i}",
            "url": f"http://paper{i}.com",
            "analysis": {
                "research_problem": "Problem X",
                "methodology": "Method Y",
                "key_findings": "Result Z",
                "novelty_assessment": "High"
            }
        } for i in range(6)
    ]

    # Mock behavior: 0.5s delay per call
    def mock_query_groq(prompt, **kwargs):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

    mock_llm.side_effect = mock_query_groq

    print(f"Benchmarking Stage 4 with {len(analyzed_docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(analyzed_docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 took {duration:.2f} seconds.")
    print(f"Results count: {len(results)}")

    # Verify order
    all_correct = True
    for i, doc in enumerate(results):
        if doc['title'] != f"Paper {i}":
            print(f"ORDER MISMATCH at index {i}: Expected Paper {i}, got {doc['title']}")
            all_correct = False
    if all_correct:
        print("All documents in correct order.")

if __name__ == "__main__":
    benchmark_stage4()
