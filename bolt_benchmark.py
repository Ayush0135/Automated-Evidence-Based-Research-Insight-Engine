
import sys
import time
import json
import re
from unittest.mock import MagicMock

# Mock LLM and Search modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    print("Benchmarking Stage 4...")

    # Setup mock documents
    docs = []
    for i in range(6):
        docs.append({
            'title': f"Document {i}",
            'analysis': {
                'research_problem': f"Problem {i}",
                'methodology': f"Method {i}",
                'key_findings': f"Findings {i}",
                'novelty_assessment': f"Novelty {i}"
            }
        })

    topic = "Test Topic"

    # Mock query_groq to take 0.5s per call
    def mock_query_groq(prompt, **kwargs):
        time.sleep(0.5)
        # Find Document X in prompt
        match = re.search(r'Document Title: Document (\d+)', prompt)
        if match:
            doc_idx = match.group(1)
            return json.dumps({"score": 8, "strengths": f"Strength {doc_idx}", "weaknesses": "None"})
        return json.dumps({"score": 8, "strengths": "Strong", "weaknesses": "None"})

    mock_llm.query_groq.side_effect = mock_query_groq

    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 duration: {duration:.2f} seconds")

    # Verify order
    order_ok = True
    for i, res in enumerate(results):
        if f"Document {i}" not in res['title']:
            print(f"ORDER MISMATCH at index {i}: Expected Document {i}, got {res['title']}")
            order_ok = False
            break

    if order_ok:
        print("Order preserved correctly.")
    else:
        print("Order NOT preserved.")

    return duration, order_ok

if __name__ == "__main__":
    benchmark_stage4()
