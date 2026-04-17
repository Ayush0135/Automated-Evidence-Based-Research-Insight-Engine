
import sys
import time
import unittest.mock as mock
from stages.stage4_scoring import stage4_academic_scoring

# Mocking external dependencies before they are used
mock_groq = mock.MagicMock()
# sys.modules['utils.llm'] = mock.MagicMock()
# sys.modules['utils.llm'].query_groq = mock_groq

def simulate_query_groq(prompt, json_mode=False, fallback_to_others=True):
    time.sleep(0.5)  # Simulate network/inference delay
    return '{"score": 8, "strengths": "Good methodology", "weaknesses": "None"}'

def run_benchmark():
    topic = "Impact of AI on Education"
    analyzed_docs = [
        {
            "title": f"Paper {i}",
            "url": f"http://example.com/{i}",
            "analysis": {
                "research_problem": "Problem X",
                "methodology": "Method Y",
                "key_findings": "Findings Z",
                "novelty_assessment": "High"
            }
        }
        for i in range(6)
    ]

    print(f"Running Stage 4 Benchmark with {len(analyzed_docs)} documents...")

    with mock.patch('stages.stage4_scoring.query_groq', side_effect=simulate_query_groq):
        start_time = time.time()
        results = stage4_academic_scoring(analyzed_docs, topic)
        end_time = time.time()

    duration = end_time - start_time
    print(f"\nBenchmark Result:")
    print(f"Total Time: {duration:.2f} seconds")
    print(f"Results Count: {len(results)}")

    # Check if order is preserved (for future reference)
    titles = [doc['title'] for doc in results]
    expected_titles = [f"Paper {i}" for i in range(6)]
    if titles == expected_titles:
        print("Order preserved: Yes")
    else:
        print("Order preserved: No")
        print(f"Expected: {expected_titles}")
        print(f"Actual: {titles}")

if __name__ == "__main__":
    run_benchmark()
