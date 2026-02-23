import sys
import time
from unittest.mock import MagicMock, patch

# Mock the utils before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()

sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_parallelism():
    print("Testing Stage 4 Parallelism and Order Preservation...")

    # Setup mock data
    analyzed_docs = [
        {'title': f'Doc {i}', 'url': f'http://{i}.com', 'analysis': {'research_problem': 'P', 'methodology': 'M', 'key_findings': 'F', 'novelty_assessment': 'N'}}
        for i in range(5)
    ]
    topic = "Test Topic"

    # Mock query_groq to simulate a delay
    def mocked_query_groq(prompt, **kwargs):
        # Extract doc index from prompt if possible, or just sleep
        time.sleep(0.5)
        return '{"score": 8, "strengths": "S", "weaknesses": "W"}'

    mock_llm.query_groq.side_effect = mocked_query_groq

    start_time = time.time()
    results = stage4_academic_scoring(analyzed_docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Duration for 5 docs: {duration:.2f} seconds")

    # Check order
    for i, doc in enumerate(results):
        print(f"Result {i}: {doc['title']}")
        if doc['title'] != f'Doc {i}':
            print(f"ORDER MISMATCH at index {i}!")
            return False

    if duration > 2.0:
        print("Stage 4 appears to be SEQUENTIAL.")
    elif duration < 1.5:
        print("Stage 4 appears to be PARALLEL.")
    else:
        print("Stage 4 parallelism is UNKNOWN.")

    return True

if __name__ == "__main__":
    test_stage4_parallelism()
