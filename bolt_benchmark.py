
import time
import sys
from unittest.mock import MagicMock

# Mocking LLM and Search to avoid API calls and allow controlled delays
mock_llm = MagicMock()
mock_search = MagicMock()

# Inject mocks into sys.modules before importing stages
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Mock the query_groq function specifically
def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

mock_llm.query_groq.side_effect = mock_query_groq

from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_performance():
    # 2. Create 6 mock analyzed documents
    mock_docs = []
    for i in range(6):
        mock_docs.append({
            "title": f"Paper {i}",
            "url": f"http://paper{i}.com",
            "analysis": {
                "research_problem": f"Problem {i}",
                "methodology": f"Method {i}",
                "key_findings": f"Findings {i}",
                "novelty_assessment": f"Novelty {i}"
            }
        })

    print(f"Starting Stage 4 benchmark with {len(mock_docs)} documents...")
    start_time = time.time()

    # 3. Execute Stage 4
    scored_docs = stage4_academic_scoring(mock_docs, "Quantum Computing")

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"\nStage 4 completed in {elapsed:.2f} seconds.")

    # 4. Verify Order
    ordered = all(scored_docs[i]['title'] == f"Paper {i}" for i in range(len(scored_docs)))
    print(f"Order Preserved: {ordered}")

    return elapsed, ordered

if __name__ == "__main__":
    test_stage4_performance()
