import sys
import time
from unittest.mock import MagicMock

# Mock dependencies before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

# Setup mocks to satisfy imports
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search
sys.modules['utils.llm_offline'] = MagicMock()

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_parallelism_and_order():
    print("Testing Stage 4 Parallelism and Order...")
    # Mock query_groq to simulate network delay
    def mocked_query_groq(prompt, **kwargs):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

    mock_llm.query_groq.side_effect = mocked_query_groq

    docs = [
        {'title': 'Doc 1', 'analysis': {'research_problem': 'P1'}},
        {'title': 'Doc 2', 'analysis': {'research_problem': 'P2'}},
        {'title': 'Doc 3', 'analysis': {'research_problem': 'P3'}},
    ]

    start_time = time.time()
    scored_docs = stage4_academic_scoring(docs, "topic")
    duration = time.time() - start_time

    print(f"Duration: {duration:.2f}s")
    # With 3 workers and 3 docs, it should take ~0.5s if parallel, ~1.5s if sequential
    assert duration < 1.0, f"Stage 4 should be parallel, took {duration:.2f}s"

    # Check order
    titles = [d['title'] for d in scored_docs]
    print(f"Titles order: {titles}")
    assert titles == ['Doc 1', 'Doc 2', 'Doc 3'], "Order should be preserved in Stage 4"
    print("Stage 4 OK")

def test_stage3_order():
    print("\nTesting Stage 3 Order...")
    # Mock query_gemini to return fixed analysis
    mock_llm.query_gemini.return_value = '{"research_problem": "P"}'

    docs = [
        {'title': 'Doc 1', 'raw_text': 'small text 1'},
        {'title': 'Doc 2', 'raw_text': 'small text 2'},
        {'title': 'Doc 3', 'raw_text': 'small text 3'},
    ]

    # We want to check if the order in which they are returned matches the input
    # Even if they complete at different times (simulated by sleep)
    def mocked_analyze(doc):
        # Doc 1 takes longer but should still be first in results
        if doc['title'] == 'Doc 1':
            time.sleep(0.3)
        return doc

    # We need to monkeypatch the internal analyze_single_document in stage3_analysis
    import stages.stage3_analysis
    original_analyze = stages.stage3_analysis.analyze_single_document
    stages.stage3_analysis.analyze_single_document = mocked_analyze

    try:
        analyzed_docs = stage3_document_analysis(docs)
        titles = [d['title'] for d in analyzed_docs]
        print(f"Titles order: {titles}")
        assert titles == ['Doc 1', 'Doc 2', 'Doc 3'], "Order should be preserved in Stage 3"
    finally:
        stages.stage3_analysis.analyze_single_document = original_analyze

    print("Stage 3 OK")

def test_stage2_order():
    print("\nTesting Stage 2 Order...")
    mock_search.google_search.return_value = [
        {'link': 'url1', 'title': 'Research Topic 1', 'snippet': 'Snippet 1'},
        {'link': 'url2', 'title': 'Research Topic 2', 'snippet': 'Snippet 2'},
    ]
    mock_search.download_and_parse.side_effect = lambda url: f"Text for {url} content with enough length to pass filter. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." * 10

    decomposition = {
        'subtopics': [{'name': 'Research', 'search_queries': ['Q1']}]
    }

    # Similar to stage 3, we check if download order follows search result order
    docs = stage2_document_discovery(decomposition)
    titles = [d['title'] for d in docs]
    print(f"Titles order: {titles}")
    assert titles == ['Research Topic 1', 'Research Topic 2'], f"Order should be preserved in Stage 2. Got: {titles}"
    print("Stage 2 OK")

if __name__ == "__main__":
    try:
        test_stage4_parallelism_and_order()
        test_stage3_order()
        test_stage2_order()
        print("\nALL VERIFICATIONS PASSED!")
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
