import time
import sys
from unittest.mock import MagicMock

# Mocking internal modules before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()

sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    print("Benchmarking Stage 4...")

    # Mocking query_groq to simulate delay and return specific score for each doc
    def mock_query_groq(prompt, **kwargs):
        # Extract doc title from prompt to return unique score
        import re
        match = re.search(r"Document Title: (Doc \d+)", prompt)
        doc_id = match.group(1) if match else "Unknown"
        time.sleep(0.5)  # Simulate LLM latency
        score = int(doc_id.split()[-1]) if "Doc" in doc_id else 0
        return f'{{"score": {score}, "strengths": "Good", "weaknesses": "None"}}'

    mock_llm.query_groq.side_effect = mock_query_groq

    docs = []
    for i in range(6):
        docs.append({
            "title": f"Doc {i}",
            "analysis": {
                "research_problem": "Problem",
                "methodology": "Method",
                "key_findings": "Findings",
                "novelty_assessment": "Novelty"
            }
        })

    start_time = time.time()
    scored_docs = stage4_academic_scoring(docs, "Topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 took: {duration:.2f}s")

    # Check order
    order_ok = True
    for i, doc in enumerate(scored_docs):
        if doc['title'] != f"Doc {i}":
            print(f"ORDER MISMATCH: Expected Doc {i}, got {doc['title']}")
            order_ok = False
            break
    if order_ok:
        print("Order preserved correctly.")

    return duration, order_ok

if __name__ == "__main__":
    benchmark_stage4()
