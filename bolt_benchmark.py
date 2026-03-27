import sys
import time
import json
from unittest.mock import MagicMock, patch

# Mock the modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)  # Simulate network latency
    return json.dumps({"score": 8, "strengths": "Strong methodology", "weaknesses": "None"})

def mock_query_gemini(prompt, **kwargs):
    time.sleep(0.5)
    return json.dumps({
        "research_problem": "Problem X",
        "methodology": "Method Y",
        "key_findings": "Result Z",
        "limitations": "Limit L",
        "research_gaps": "Gap G",
        "novelty_assessment": "Novel N",
        "technical_depth_score": 8,
        "missing_entities": "None"
    })

def mock_google_search(query, num_results=5):
    return [{"link": f"http://example.com/{i}", "title": f"Doc {i} for {query}", "snippet": f"Snippet {i} containing topic keywords"} for i in range(num_results)]

def mock_download_and_parse(url):
    return "This is a long enough text to pass the length filter and be considered a valid paper content for testing purposes." * 10

mock_llm.query_groq.side_effect = mock_query_groq
mock_llm.query_gemini.side_effect = mock_query_gemini
mock_llm.query_stage.side_effect = lambda stage, prompt: mock_query_gemini(prompt) if stage == "analysis" else mock_query_groq(prompt)
mock_search.google_search.side_effect = mock_google_search
mock_search.download_and_parse.side_effect = mock_download_and_parse

def benchmark_stage4():
    print("\n--- Benchmarking Stage 4 (Sequential) ---")
    docs = [{"title": f"Document {i}", "analysis": {"key": "value"}} for i in range(6)]
    start_time = time.time()
    results = stage4_academic_scoring(docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 Duration: {duration:.2f}s")

    # Verify order
    order_ok = all(results[i]['title'] == f"Document {i}" for i in range(len(results)))
    print(f"Order Preserved: {order_ok}")
    return duration, order_ok

def verify_stage2_order():
    print("\n--- Verifying Stage 2 Order ---")
    decomp = {
        'subtopics': [
            {'name': 'Topic A', 'search_queries': ['Query A1', 'Query A2']},
            {'name': 'Topic B', 'search_queries': ['Query B1']}
        ]
    }
    # With as_completed, the order of search_candidates and all_documents might be scrambled.
    results = stage2_document_discovery(decomp)
    # Since we want to check if it's currently scrambled, we just log the titles.
    titles = [d['title'] for d in results]
    print(f"Retrieved Titles: {titles}")

def verify_stage3_order():
    print("\n--- Verifying Stage 3 Order ---")
    docs = [{"title": f"Doc {i}", "raw_text": mock_download_and_parse("")} for i in range(5)]
    results = stage3_document_analysis(docs)
    titles = [d['title'] for d in results]
    print(f"Analyzed Titles: {titles}")
    order_ok = all(results[i]['title'] == f"Doc {i}" for i in range(len(results)))
    print(f"Order Preserved: {order_ok}")

if __name__ == "__main__":
    benchmark_stage4()
    verify_stage2_order()
    verify_stage3_order()
