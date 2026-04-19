
import time
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock dependencies before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()

sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def setup_mocks():
    # Stage 2 mocks
    def slow_search(query, num_results=5):
        # Extract subtopic name from query if possible, or just use part of query
        # In the test below, subtopic names are 'Topic' (from 'Topic A' and 'Topic B')
        time.sleep(0.1)
        return [{'link': f'http://example.com/{query}/{i}', 'title': f'Topic Academic Paper {query} {i}', 'snippet': f'Extremely relevant results for Topic research.'} for i in range(num_results)]

    mock_search.google_search.side_effect = slow_search

    def slow_download(url):
        time.sleep(0.2)
        # Return a long string to pass Stage 2 filter and cause chunking in Stage 3 for one doc
        if "large" in url:
            return "Academic Content " * 2000 # ~26,000 chars
        return "Academic Content " * 100 # ~1300 chars

    mock_search.download_and_parse.side_effect = slow_download

    # Stage 3/4 mocks
    def slow_llm_query(prompt, **kwargs):
        time.sleep(0.5)
        if "JSON" in prompt or "Output Format" in prompt:
             return '{"score": 8, "research_problem": "test", "methodology": "test", "key_findings": "test", "novelty_assessment": "test", "technical_depth_score": 8}'
        return "Summary of chunk"

    mock_llm.query_gemini.side_effect = slow_llm_query
    mock_llm.query_groq.side_effect = slow_llm_query

def test_stage2_order():
    print("\nTesting Stage 2 Order Preservation...")
    decomposition = {
        'subtopics': [
            {'name': 'Topic A', 'search_queries': ['Query A1']},
            {'name': 'Topic B', 'search_queries': ['Query B1']}
        ]
    }
    # We want to see if the order of queries is preserved in results
    # Since it uses as_completed, it might be scrambled.
    start_time = time.time()
    docs = stage2_document_discovery(decomposition)
    duration = time.time() - start_time
    print(f"Stage 2 took {duration:.2f}s")

    titles = [d['title'] for d in docs]
    print(f"Result titles: {titles}")
    # With as_completed, Query B1 might finish before Query A1 if we are unlucky or have many queries.
    # In this mock they have same delay, so it depends on thread scheduling.

def test_stage3_order():
    print("\nTesting Stage 3 Order Preservation...")
    docs = [
        {'title': 'Doc 1', 'raw_text': 'Small doc', 'url': 'http://example.com/small'},
        {'title': 'Doc 2', 'raw_text': 'Large doc ' * 2000, 'url': 'http://example.com/large'}
    ]
    start_time = time.time()
    analyzed = stage3_document_analysis(docs)
    duration = time.time() - start_time
    print(f"Stage 3 took {duration:.2f}s")

    # Check if Doc 1 is still first
    if analyzed[0]['title'] != 'Doc 1':
        print("ALERT: Stage 3 documents are out of order!")
    else:
        print("Stage 3 documents are in order.")

def test_stage4_performance():
    print("\nTesting Stage 4 Performance (Baseline)...")
    docs = [
        {'title': f'Doc {i}', 'analysis': {'research_problem': 'p'}, 'url': f'u{i}'} for i in range(4)
    ]
    start_time = time.time()
    scored = stage4_academic_scoring(docs, "Test Topic")
    duration = time.time() - start_time
    print(f"Stage 4 took {duration:.2f}s")
    # Expected: 4 docs * 0.5s = ~2s (since it is currently sequential)

if __name__ == "__main__":
    setup_mocks()
    test_stage2_order()
    test_stage3_order()
    test_stage4_performance()
