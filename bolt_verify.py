import sys
import time
from unittest.mock import MagicMock

# Mock the modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Set up mock returns
# Each call takes 0.5s to simulate I/O
mock_llm.query_groq.side_effect = lambda *args, **kwargs: (time.sleep(0.5), '{"score": 8, "strengths": "good", "weaknesses": "none"}')[1]
mock_llm.query_gemini.side_effect = lambda *args, **kwargs: (time.sleep(0.5), '{"research_problem": "abc", "methodology": "def", "key_findings": "ghi", "novelty_assessment": "jkl", "technical_depth_score": 5, "missing_entities": "none", "research_gaps": "none", "limitations": "none"}')[1]

mock_search.google_search.return_value = [{'link': f'http://example.com/{i}', 'title': f'Title {i}', 'snippet': f'Snippet {i}'} for i in range(5)]
mock_search.download_and_parse.return_value = "This is a long enough text to pass the 500 character check. " * 10

from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import stage3_document_analysis
from stages.stage2_discovery import stage2_document_discovery

def test_stage4_performance():
    print("\nVerifying Stage 4 Parallelism and Order...")
    docs = [{'title': f'Doc {i}', 'analysis': {'research_problem': 'P'}} for i in range(6)]
    start = time.time()
    scored = stage4_academic_scoring(docs, "topic")
    end = time.time()
    duration = end - start
    print(f"Stage 4 (6 docs, 0.5s each) took {duration:.2f} seconds.")
    # Sequential would take 3.0s
    # Parallel with 3 workers should take ~1.0s (2 rounds of 3)
    # We allow some overhead (up to 2.0s) but it should be much less than 3s.
    assert duration < 2.5, f"Stage 4 is too slow: {duration:.2f}s (Likely still sequential)"
    assert len(scored) == 6
    # Check order
    for i, doc in enumerate(scored):
        if doc['title'] != f'Doc {i}':
            raise AssertionError(f"Order mismatched at {i}: Expected Doc {i}, got {doc['title']}")
    print("Stage 4 Performance and Order Check: PASSED")

def test_stage3_order():
    print("\nVerifying Stage 3 Order...")
    docs = [{'title': f'Doc {i}', 'raw_text': 'short text'} for i in range(5)]
    analyzed = stage3_document_analysis(docs)
    for i, doc in enumerate(analyzed):
         if doc['title'] != f'Doc {i}':
             raise AssertionError(f"Order mismatched at index {i}: expected Doc {i}, got {doc['title']}")
    print("Stage 3 Order Check: PASSED")

def test_stage2_order():
    print("\nVerifying Stage 2 Order...")
    decomp = {'subtopics': [{'name': 'Sub 1', 'search_queries': ['Q1']}]}
    docs = stage2_document_discovery(decomp)
    # google_search returns 5 items
    assert len(docs) == 5
    for i, doc in enumerate(docs):
        if doc['title'] != f'Title {i}':
             raise AssertionError(f"Order mismatched at index {i}: expected Title {i}, got {doc['title']}")
    print("Stage 2 Order Check: PASSED")

if __name__ == "__main__":
    try:
        test_stage2_order()
        test_stage3_order()
        test_stage4_performance()
        print("\nALL BOLT VERIFICATIONS PASSED! ⚡")
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
