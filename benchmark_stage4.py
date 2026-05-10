import sys
import time
from unittest.mock import MagicMock

# Mock dependencies before importing the stage
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

def mock_query_groq(prompt, json_mode=True, fallback_to_others=True):
    time.sleep(0.5)
    return '{"score": 8, "strengths": "Good methodology", "weaknesses": "Small sample size"}'

mock_llm.query_groq = mock_query_groq

from stages.stage4_scoring import stage4_academic_scoring

def run_benchmark():
    topic = "Quantum Computing"
    docs = []
    for i in range(10):
        docs.append({
            "title": f"Paper {i}",
            "analysis": {
                "research_problem": "Problem X",
                "methodology": "Method Y",
                "key_findings": "Result Z",
                "novelty_assessment": "High"
            }
        })

    print(f"Starting benchmark for Stage 4 with {len(docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 completed in {duration:.2f} seconds.")

    # Verify order
    for i, res in enumerate(results):
        if res['title'] != f"Paper {i}":
            print(f"ERROR: Order mismatch at index {i}. Expected Paper {i}, got {res['title']}")
            return
    print("Order preservation verified.")

if __name__ == "__main__":
    run_benchmark()
