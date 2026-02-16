
import sys
import os
import time
import json
from unittest.mock import MagicMock, patch

# Mock the utilities before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

# Mocking utils.llm and utils.search
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def test_stage2_order():
    print("\nTesting Stage 2 Order Preservation...")
    decomposition = {
        'subtopics': [
            {'name': 'TopicA', 'search_queries': ['query A1', 'query A2']},
            {'name': 'TopicB', 'search_queries': ['query B1']}
        ]
    }

    # Mock search to return results based on query name
    # Include subtopic name in title/snippet to pass relevance check
    def side_effect_search(query, num_results=6):
        time.sleep(0.1) # Simulate network delay
        subtopic = "TopicA" if "A" in query else "TopicB"
        return [{'link': f'url_{query}_{i}', 'title': f'Title {query} {subtopic} {i}', 'snippet': f'Academic paper about {subtopic}'} for i in range(2)]

    mock_search.google_search.side_effect = side_effect_search

    # Mock download to return based on URL
    def side_effect_download(url):
        return "This is a long enough text to pass the length check of 500 characters. " * 10

    mock_search.download_and_parse.side_effect = side_effect_download

    docs = stage2_document_discovery(decomposition)

    # Check if order matches query submission order: A1, A2, B1
    expected_order_prefixes = ['Title query A1', 'Title query A2', 'Title query B1']
    actual_order = [d['title'] for d in docs]

    print(f"Actual titles: {[t[:30] for t in actual_order]}")

    assert len(docs) == 6, f"Expected 6 documents, got {len(docs)}"

    for i, prefix in enumerate(expected_order_prefixes):
        # Check that they appear in blocks of 2 (since each query returns 2)
        assert prefix in actual_order[i*2], f"Missing {prefix} at index {i*2}"
        assert prefix in actual_order[i*2 + 1], f"Missing {prefix} at index {i*2+1}"

    print("Stage 2 Order Preserved!")

def test_stage3_order():
    print("\nTesting Stage 3 Order Preservation...")
    docs = [
        {'title': 'Doc 1', 'raw_text': 'Text 1 ' * 100},
        {'title': 'Doc 2', 'raw_text': 'Text 2 ' * 100},
        {'title': 'Doc 3', 'raw_text': 'Text 3 ' * 100}
    ]

    def side_effect_gemini(prompt, **kwargs):
        # Simulate variable delay to test if as_completed would scramble it
        if "Doc 1" in prompt: time.sleep(0.3)
        if "Doc 2" in prompt: time.sleep(0.1)
        if "Doc 3" in prompt: time.sleep(0.05)

        return json.dumps({
            "research_problem": "Problem",
            "methodology": "Method",
            "key_findings": "Findings",
            "limitations": "Lim",
            "research_gaps": "Gap",
            "novelty_assessment": "Nov",
            "technical_depth_score": 5,
            "missing_entities": "None"
        })

    mock_llm.query_gemini.side_effect = side_effect_gemini

    analyzed = stage3_document_analysis(docs)

    actual_titles = [d['title'] for d in analyzed]
    print(f"Actual order: {actual_titles}")
    assert actual_titles == ['Doc 1', 'Doc 2', 'Doc 3'], f"Order scrambled: {actual_titles}"
    print("Stage 3 Order Preserved!")

def test_stage4_parallel_and_order():
    print("\nTesting Stage 4 Parallelization and Order Preservation...")
    docs = [
        {'title': 'Doc A', 'analysis': {'research_problem': 'P1'}},
        {'title': 'Doc B', 'analysis': {'research_problem': 'P2'}},
        {'title': 'Doc C', 'analysis': {'research_problem': 'P3'}}
    ]

    def side_effect_groq(prompt, **kwargs):
        if "Doc A" in prompt: time.sleep(0.3)
        if "Doc B" in prompt: time.sleep(0.1)
        if "Doc C" in prompt: time.sleep(0.05)
        return json.dumps({"score": 8, "strengths": "S", "weaknesses": "W"})

    mock_llm.query_groq.side_effect = side_effect_groq

    start_time = time.time()
    scored = stage4_academic_scoring(docs, "topic")
    end_time = time.time()

    actual_titles = [d['title'] for d in scored]
    print(f"Actual order: {actual_titles}")
    assert actual_titles == ['Doc A', 'Doc B', 'Doc C'], f"Order scrambled: {actual_titles}"

    duration = end_time - start_time
    print(f"Duration: {duration:.2f}s")
    # If sequential, it would be 0.3 + 0.1 + 0.05 = 0.45s
    # If parallel with 3 workers, it should be around max(0.3, 0.1, 0.05) = 0.3s
    assert duration < 0.4, f"Does not seem parallelized: {duration:.2f}s"
    print("Stage 4 Parallelized and Order Preserved!")

if __name__ == "__main__":
    try:
        test_stage2_order()
        test_stage3_order()
        test_stage4_parallel_and_order()
        print("\nALL VERIFICATIONS PASSED!")
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
