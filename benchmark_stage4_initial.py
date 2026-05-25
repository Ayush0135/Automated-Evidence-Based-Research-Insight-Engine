import time
import sys
import os
from unittest.mock import MagicMock, patch

# Mocking necessary modules before importing stage4
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

# Now import the function
from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, **kwargs):
    time.sleep(1)  # Simulate 1 second latency per call
    return '{"score": 8, "strengths": "s", "weaknesses": "w"}'

def main():
    docs = []
    for i in range(5):
        docs.append({
            'title': f"Research Paper {i}",
            'analysis': {
                'research_problem': 'Problem',
                'methodology': 'Method',
                'key_findings': 'Findings',
                'novelty_assessment': 'Novelty'
            }
        })

    topic = "Test Topic"

    print(f"Benchmarking Stage 4 with 5 documents (simulated 1s latency per call)...")

    with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
        start_time = time.time()
        results = stage4_academic_scoring(docs, topic)
        end_time = time.time()

    duration = end_time - start_time
    print(f"Total time: {duration:.2f} seconds")

    # Verify results
    if len(results) == 5:
        print("Success: All 5 documents scored.")
    else:
        print(f"Failure: Only {len(results)} documents scored.")

    # Verify order preservation (important for research relevance)
    for i, res in enumerate(results):
        if res['title'] != f"Research Paper {i}":
             print(f"Failure: Order not preserved at index {i}. Expected Research Paper {i}, got {res['title']}")

if __name__ == "__main__":
    main()
