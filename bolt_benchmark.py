
import sys
import time
import json
from unittest.mock import MagicMock

# Create a mock for utils.llm
mock_llm = MagicMock()

# Setup side effect for query_groq with delay
def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)
    return json.dumps({"score": 8, "strengths": "s", "weaknesses": "w"})

mock_llm.query_groq = mock_query_groq

# Patch sys.modules BEFORE importing stage4
sys.modules['utils.llm'] = mock_llm

# Mock utils.search as well
sys.modules['utils.search'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    print("Benchmarking Stage 4: Academic Scoring")

    docs = [
        {"title": f"Doc {i}", "url": f"http://test.com/{i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
        for i in range(6)
    ]
    topic = "Test Topic"

    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    duration = time.time() - start_time

    print(f"Stage 4 duration: {duration:.2f}s")

    result_titles = [d['title'] for d in results]
    expected_titles = [d['title'] for d in docs]

    if result_titles == expected_titles:
        print("Order preserved: YES")
    else:
        print(f"Order preserved: NO (Expected {expected_titles}, got {result_titles})")

    return duration

if __name__ == "__main__":
    benchmark_stage4()
