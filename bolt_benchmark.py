import sys
import os
import time
from unittest.mock import MagicMock

# Mock dependencies before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Define mock behavior
def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

def mock_query_gemini(prompt, **kwargs):
    time.sleep(0.3)
    return '{"research_problem": "Problem", "methodology": "Method", "key_findings": "Findings", "novelty_assessment": "Novelty"}'

def mock_google_search(query, num_results=6):
    time.sleep(0.2)
    # Include subtopic name in title to pass the filter
    # The filter checks if keywords from subtopic name are in title or snippet
    return [{'link': f'http://example.com/{i}', 'title': f'Paper {i} Research', 'snippet': f'Snippet {i}'} for i in range(num_results)]

def mock_download_and_parse(url):
    time.sleep(0.4)
    return "Relevant research content " * 100

mock_llm.query_groq = mock_query_groq
mock_llm.query_gemini = mock_query_gemini
mock_llm.query_stage = lambda stage, prompt: mock_query_gemini(prompt)
mock_search.google_search = mock_google_search
mock_search.download_and_parse = mock_download_and_parse

from stages.stage4_scoring import stage4_academic_scoring
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis

def benchmark_stage4():
    print("\nBenchmarking Stage 4 (Parallel)...")
    docs = [
        {
            "title": f"Paper {i}",
            "analysis": {
                "research_problem": "Problem",
                "methodology": "Method",
                "key_findings": "Findings",
                "novelty_assessment": "Novelty"
            }
        } for i in range(6)
    ]

    start_time = time.time()
    scored_docs = stage4_academic_scoring(docs, "Quantum Computing")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 Duration: {duration:.2f} seconds")

    # Verify Order
    for i, doc in enumerate(scored_docs):
        if doc['title'] != f"Paper {i}":
            print(f"CRITICAL: Order mismatch at index {i}. Expected Paper {i}, got {doc['title']}")
            return False
    print("Stage 4: Order preserved.")
    return duration

def benchmark_stage2():
    print("\nBenchmarking Stage 2 (Parallel)...")
    decomposition = {
        'subtopics': [
            {'name': 'Research', 'search_queries': ['query 1', 'query 2']}
        ]
    }

    start_time = time.time()
    docs = stage2_document_discovery(decomposition)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 2 Duration: {duration:.2f} seconds")

    # Verify Order
    # We expect 6 docs from query 1 then 6 docs from query 2 (but seen_urls will filter them if identical)
    # In our mock they are identical URLs. So we expect 6 unique docs.
    print(f"Retrieved {len(docs)} unique documents.")
    if len(docs) > 0:
        print("Stage 2: Completed.")
    else:
        print("Stage 2: FAILED to retrieve documents.")
    return duration

def benchmark_stage3():
    print("\nBenchmarking Stage 3 (Parallel)...")
    docs = [
        {
            "title": f"Paper {i}",
            "raw_text": "Short content " * 10
        } for i in range(4)
    ]

    # Add a large document to test chunking order
    # ~26000 chars will result in 3 chunks (12000 size, 500 overlap)
    # Chunk 1: 0-12000
    # Chunk 2: 11500-23500
    # Chunk 3: 23000-26000
    docs.append({
        "title": "Large Paper",
        "raw_text": "Large content " * 2000
    })

    start_time = time.time()
    analyzed_docs = stage3_document_analysis(docs)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 3 Duration: {duration:.2f} seconds")

    # Verify Order
    for i, doc in enumerate(analyzed_docs):
        expected_title = f"Paper {i}" if i < 4 else "Large Paper"
        if doc['title'] != expected_title:
            print(f"CRITICAL: Order mismatch at index {i}. Expected {expected_title}, got {doc['title']}")
            return False
    print("Stage 3: Order preserved.")
    return duration

if __name__ == "__main__":
    s2 = benchmark_stage2()
    s3 = benchmark_stage3()
    s4 = benchmark_stage4()

    print("\n--- Benchmark Summary ---")
    print(f"Stage 2: {s2:.2f}s")
    print(f"Stage 3: {s3:.2f}s")
    print(f"Stage 4: {s4:.2f}s")

    if s4 < 1.5:
        print("\nSUCCESS: Stage 4 shows significant speedup (Parallelism working).")
    else:
        print("\nFAILURE: Stage 4 is too slow.")
