
import time
import sys
from unittest.mock import MagicMock

# Mock internal modules before importing stages
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm
mock_search = MagicMock()
sys.modules['utils.search'] = mock_search

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)  # Simulate LLM latency
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

# Configure mock before import
mock_llm.query_groq.side_effect = mock_query_groq

from stages.stage4_scoring import stage4_academic_scoring

def run_benchmark():
    print("Running Stage 4 Benchmark...")

    docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
        for i in range(6)
    ]
    topic = "Test Topic"

    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Processed {len(results)} documents in {duration:.2f} seconds.")

if __name__ == "__main__":
    run_benchmark()
