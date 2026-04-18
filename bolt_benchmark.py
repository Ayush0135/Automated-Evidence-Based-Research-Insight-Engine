
import time
import sys
import json
import unittest.mock as mock
from concurrent.futures import ThreadPoolExecutor

# Mocking external dependencies before importing stages
mock_llm = mock.MagicMock()
mock_search = mock.MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Now we can import the stages
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def mock_query_gemini(prompt, **kwargs):
    time.sleep(0.5)  # Simulate LLM latency
    # If it's a chunk analysis, return something simple
    if "Analyze this segment" in prompt:
        return f"Summary for chunk in prompt: {prompt[:50]}..."

    # If it's the final analysis
    return json.dumps({
        "research_problem": "Problem",
        "methodology": "Method",
        "key_findings": "Findings",
        "limitations": "Limit",
        "research_gaps": "Gap",
        "novelty_assessment": "Novelty",
        "technical_depth_score": 8,
        "missing_entities": "None"
    })

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5)  # Simulate LLM latency
    return json.dumps({
        "score": 8,
        "strengths": "Good",
        "weaknesses": "None"
    })

def mock_google_search(query, num_results=5):
    time.sleep(0.2)
    # Include 'topic' in title to pass Stage 2 relevance filter
    return [
        {"link": f"http://example.com/{i}", "title": f"Topic Doc {i} for {query}", "snippet": f"Snippet {i}"}
        for i in range(num_results)
    ]

def mock_download_and_parse(url):
    time.sleep(0.3)
    # Return long enough text to pass filters
    return "This is a long academic text that should pass the minimum length filter of five hundred characters. " * 10

def run_benchmark():
    mock_llm.query_gemini.side_effect = mock_query_gemini
    mock_llm.query_groq.side_effect = mock_query_groq
    mock_search.google_search.side_effect = mock_google_search
    mock_search.download_and_parse.side_effect = mock_download_and_parse

    print("=== BASELINE BENCHMARK ===")

    # Stage 2 Benchmark
    print("\nBenchmarking Stage 2...")
    decomposition = {
        'subtopics': [
            {'name': 'Topic 1', 'search_queries': ['query 1', 'query 2']}
        ]
    }
    start = time.time()
    docs = stage2_document_discovery(decomposition)
    end = time.time()
    print(f"Stage 2 Time: {end - start:.2f}s")
    print(f"Stage 2 Docs: {len(docs)}")

    # Verify Order in Stage 2 (Check if docs are in search result order)
    # Search candidates are added to search_candidates list in order they come from as_completed(search_queries)
    # Then they are processed by as_completed(process_search_item)
    # This likely results in randomized order.

    # Stage 3 Benchmark
    print("\nBenchmarking Stage 3...")
    # Use a few documents with long text to trigger chunking
    # We want enough chunks to see if parallel chunking works.
    # 3000 * 5 = 15000 chars > 12000.
    # Let's use 6000 * 5 = 30000 chars to get ~3 chunks.
    test_docs = [
        {"title": f"Doc {i}", "url": f"url_{i}", "raw_text": "ChunkText " * 6000}
        for i in range(4)
    ]
    start = time.time()
    analyzed_docs = stage3_document_analysis(test_docs)
    end = time.time()
    print(f"Stage 3 Time: {end - start:.2f}s")

    # Stage 4 Benchmark
    print("\nBenchmarking Stage 4...")
    start = time.time()
    scored_docs = stage4_academic_scoring(analyzed_docs, "topic")
    end = time.time()
    print(f"Stage 4 Time: {end - start:.2f}s")

    # Verify Order Preservation
    print("\nVerifying Order Preservation...")

    # Check Stage 3 output order vs input order
    input_titles = [d['title'] for d in test_docs]
    output_titles = [d['title'] for d in analyzed_docs]
    print(f"Stage 3 Input:  {input_titles}")
    print(f"Stage 3 Output: {output_titles}")
    if input_titles == output_titles:
        print("✅ Stage 3 preserved document order.")
    else:
        print("❌ Stage 3 SCRAMBLED document order.")

    # Check Stage 4 output order vs input order
    input_titles_4 = [d['title'] for d in analyzed_docs]
    output_titles_4 = [d['title'] for d in scored_docs]
    print(f"Stage 4 Input:  {input_titles_4}")
    print(f"Stage 4 Output: {output_titles_4}")
    if input_titles_4 == output_titles_4:
        print("✅ Stage 4 preserved document order.")
    else:
        print("❌ Stage 4 SCRAMBLED document order.")

if __name__ == "__main__":
    run_benchmark()
