import time
import sys
from unittest.mock import MagicMock, patch

# Mock dependencies before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()

sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def test_stage2_order():
    print("\n>>> Testing Stage 2 Order Preservation")
    # Subtopic names will be "Topic A" and "Topic B"
    # Keywords (len > 3) will be "Topic"

    mock_search.google_search.side_effect = lambda q, num_results: [
        {'link': f'url_{q}_{i}', 'title': f'Title {q} {i} Topic', 'snippet': f'Snippet {q} {i}'} for i in range(2)
    ]
    mock_search.download_and_parse.side_effect = lambda url: f"Full text for {url} " + "A" * 600

    decomposition = {
        'subtopics': [
            {'name': 'Topic A', 'search_queries': ['query A1', 'query A2']},
            {'name': 'Topic B', 'search_queries': ['query B1']}
        ]
    }

    start = time.time()
    docs = stage2_document_discovery(decomposition)
    end = time.time()

    print(f"Stage 2 took {end-start:.2f}s")
    urls = [d['url'] for d in docs]
    print(f"URLs in order: {urls}")

def test_stage3_order():
    print("\n>>> Testing Stage 3 Order Preservation")
    mock_llm.query_gemini.side_effect = lambda p, **kwargs: '{"research_problem": "p", "methodology": "m", "key_findings": "f", "limitations": "l", "research_gaps": "g", "novelty_assessment": "n", "technical_depth_score": 5, "missing_entities": "e"}'

    docs = [
        {'title': f'Doc {i}', 'url': f'url_{i}', 'raw_text': 'Some text ' + str(i)} for i in range(5)
    ]

    start = time.time()
    analyzed = stage3_document_analysis(docs)
    end = time.time()

    print(f"Stage 3 took {end-start:.2f}s")
    titles = [d['title'] for d in analyzed]
    print(f"Titles in order: {titles}")

def test_stage4_parallel_and_order():
    print("\n>>> Testing Stage 4 Parallelism and Order")

    def slow_query(p, **kwargs):
        time.sleep(1)
        return '{"score": 8, "strengths": "s", "weaknesses": "w"}'

    mock_llm.query_groq.side_effect = slow_query

    docs = [
        {'title': f'Doc {i}', 'url': f'url_{i}', 'analysis': {'research_problem': 'p'}} for i in range(6)
    ]

    start = time.time()
    scored = stage4_academic_scoring(docs, "topic")
    end = time.time()

    duration = end - start
    print(f"Stage 4 took {duration:.2f}s")
    titles = [d['title'] for d in scored]
    print(f"Titles in order: {titles}")

    if duration > 5:
        print("RESULT: Stage 4 is SEQUENTIAL (Slow)")
    elif duration < 3:
        print("RESULT: Stage 4 is PARALLEL (Fast)")
    else:
        print(f"RESULT: Stage 4 duration {duration:.2f}s is ambiguous")

if __name__ == "__main__":
    test_stage2_order()
    test_stage3_order()
    test_stage4_parallel_and_order()
