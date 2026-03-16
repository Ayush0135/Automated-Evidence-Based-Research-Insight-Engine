
import sys
import time
import json
from unittest.mock import MagicMock, patch

# Mock modules before importing stages
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

mock_search = MagicMock()
sys.modules['utils.search'] = mock_search

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_performance_and_order():
    print("\n--- Testing Stage 4 ---")
    docs = [
        {'title': f'Doc {i}', 'analysis': {'research_problem': 'p', 'methodology': 'm', 'key_findings': 'f', 'novelty_assessment': 'n'}}
        for i in range(5)
    ]

    def slow_query_groq(prompt, **kwargs):
        time.sleep(0.2)
        return json.dumps({'score': 8, 'strengths': 's', 'weaknesses': 'w'})

    mock_llm.query_groq.side_effect = slow_query_groq

    start = time.time()
    scored_docs = stage4_academic_scoring(docs, "topic")
    end = time.time()

    duration = end - start
    print(f"Stage 4 duration: {duration:.2f}s")

    titles = [d['title'] for d in scored_docs]
    print(f"Order: {titles}")
    expected_titles = [f'Doc {i}' for i in range(5)]

    if titles == expected_titles:
        print("✅ Order preserved")
    else:
        print("❌ Order SCRAMBLED")

def test_stage3_order():
    print("\n--- Testing Stage 3 ---")
    docs = [
        {'title': f'Doc {i}', 'raw_text': 'This is some text that is short.'}
        for i in range(5)
    ]

    # To test chunk order, we need a long doc
    long_doc = {
        'title': 'Long Doc',
        'raw_text': 'A' * 30000 # Will result in multiple chunks
    }
    docs.append(long_doc)

    def slow_query_gemini(prompt, **kwargs):
        # Return something different for chunks vs doc analysis if needed
        # But for order testing, just a delay
        if "Doc 0" in prompt:
            time.sleep(0.3)
        else:
            time.sleep(0.1)

        if "Analyze this segment" in prompt:
            # Extract part number if possible to simulate out-of-order completion
            import re
            match = re.search(r'Part (\d+)', prompt)
            part = match.group(1) if match else "X"
            return f"Summary of Part {part}"

        return json.dumps({
            "research_problem": "p",
            "methodology": "m",
            "key_findings": "f",
            "limitations": "l",
            "research_gaps": "g",
            "novelty_assessment": "n",
            "technical_depth_score": 5,
            "missing_entities": "none"
        })

    mock_llm.query_gemini.side_effect = slow_query_gemini

    start = time.time()
    analyzed_docs = stage3_document_analysis(docs)
    end = time.time()

    print(f"Stage 3 duration: {end - start:.2f}s")
    titles = [d['title'] for d in analyzed_docs]
    print(f"Doc Order: {titles}")

    # Check Long Doc analysis to see if chunks were joined in order
    long_doc_result = next(d for d in analyzed_docs if d['title'] == 'Long Doc')
    # Analysis prompt context for Stage 3 uses text_context which is "\n".join(chunk_summaries)
    # We can't easily see text_context without modifying stage3, but we can see if as_completed was used.

    # If titles are not Doc 0, 1, 2, 3, 4, Long Doc, then order is scrambled.
    expected_titles = [f'Doc {i}' for i in range(5)] + ['Long Doc']
    if titles == expected_titles:
        print("✅ Doc order preserved")
    else:
        print("❌ Doc order SCRAMBLED")

def test_stage2_order():
    print("\n--- Testing Stage 2 ---")
    decomposition = {
        'subtopics': [
            {'name': 'T1', 'search_queries': ['q1', 'q2']},
            {'name': 'T2', 'search_queries': ['q3']}
        ]
    }

    def mock_google_search(query, **kwargs):
        # Queries later in the list complete faster to test scrambling
        if 'q1' in query:
            time.sleep(0.3)
        else:
            time.sleep(0.1)
        # Return results that uniquely identify the query
        return [{'link': f'url_{query}_{i}', 'title': f'Title {query} {i}', 'snippet': f'Snippet {query}'} for i in range(2)]

    def mock_download(url):
        # Downloads later in the list complete faster
        if 'q1' in url:
            time.sleep(0.3)
        else:
            time.sleep(0.1)
        return "Some long enough text to not be filtered out by stage 2 (>500 chars) " + "x" * 500

    mock_search.google_search.side_effect = mock_google_search
    mock_search.download_and_parse.side_effect = mock_download

    start = time.time()
    docs = stage2_document_discovery(decomposition)
    end = time.time()

    print(f"Stage 2 duration: {end - start:.2f}s")
    urls = [d['url'] for d in docs]
    print(f"First 5 URLs: {urls[:5]}")

    # Expected order: results from q1, then q2, then q3
    # We check if 'q1' appears before 'q2' in URLs, and 'q2' before 'q3'
    # And for each query, result 0 should appear before result 1

    is_ordered = True
    # Find indices
    try:
        idx_q1_0 = next(i for i, u in enumerate(urls) if 'q1' in u and '_0' in u)
        idx_q1_1 = next(i for i, u in enumerate(urls) if 'q1' in u and '_1' in u)
        idx_q2_0 = next(i for i, u in enumerate(urls) if 'q2' in u and '_0' in u)
        idx_q2_1 = next(i for i, u in enumerate(urls) if 'q2' in u and '_1' in u)
        idx_q3_0 = next(i for i, u in enumerate(urls) if 'q3' in u and '_0' in u)
        idx_q3_1 = next(i for i, u in enumerate(urls) if 'q3' in u and '_1' in u)

        if not (idx_q1_0 < idx_q1_1 < idx_q2_0 < idx_q2_1 < idx_q3_0 < idx_q3_1):
            is_ordered = False
    except StopIteration:
        is_ordered = False
        print("Could not find all expected URLs")

    if is_ordered:
        print("✅ Order preserved")
    else:
        print("❌ Order SCRAMBLED")

if __name__ == "__main__":
    test_stage2_order()
    test_stage3_order()
    test_stage4_performance_and_order()
