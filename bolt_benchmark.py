
import time
import sys
import json
from unittest.mock import MagicMock

# Mock dependencies before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
# Mock missing modules if needed
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import stage3_document_analysis
from stages.stage2_discovery import stage2_document_discovery

def benchmark_stage4():
    print("\n--- Benchmarking Stage 4 ---")
    docs = [{"title": f"Doc {i}", "url": f"http://test.com/{i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}} for i in range(6)]

    # Mock query_groq to take 0.5s per call
    def mock_query_groq(*args, **kwargs):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "s", "weaknesses": "w"}'

    mock_llm.query_groq.side_effect = mock_query_groq

    start_time = time.time()
    results = stage4_academic_scoring(docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 duration for 6 docs: {duration:.2f}s")

    # Verify order
    titles = [d['title'] for d in results]
    expected_titles = [f"Doc {i}" for i in range(6)]
    if titles == expected_titles:
        print("✅ Order preserved.")
    else:
        print(f"❌ Order SCRAMBLED: {titles}")

    return duration

def test_order_preservation_stage3():
    print("\n--- Testing Stage 3 Order Preservation ---")
    # Small docs to trigger chunking if > 12000, let's make them large to test chunk parallel order
    large_text = "Word " * 3000 # ~15000 chars
    docs = [{"title": f"Doc {i}", "raw_text": large_text} for i in range(2)]

    def mock_query_gemini(prompt, *args, **kwargs):
        # Identify if it's chunk analysis or final analysis
        if "Analyze this segment" in prompt:
            # Extract Part number
            import re
            match = re.search(r'Part (\d+)', prompt)
            part = match.group(1) if match else "X"
            time.sleep(0.1)
            return f"Summary of Part {part}"
        else:
            time.sleep(0.1)
            return '{"research_problem": "p", "methodology": "m", "key_findings": "f"}'

    mock_llm.query_gemini.side_effect = mock_query_gemini

    results = stage3_document_analysis(docs)

    # Verify doc order
    titles = [d['title'] for d in results]
    if titles == ["Doc 0", "Doc 1"]:
        print("✅ Document order preserved.")
    else:
        print(f"❌ Document order SCRAMBLED: {titles}")

def test_order_preservation_stage2():
    print("\n--- Testing Stage 2 Order Preservation ---")
    decomposition = {
        'subtopics': [
            {'name': 'Sub1', 'search_queries': ['q1', 'q2']}
        ]
    }

    def mock_google_search(query, **kwargs):
        time.sleep(0.1)
        # return results that include 'subtopic' keyword to pass relevance filter
        return [
            {'link': f'http://{query}.com/1', 'title': f'Result {query} 1 Sub1', 'snippet': 'snippet'},
            {'link': f'http://{query}.com/2', 'title': f'Result {query} 2 Sub1', 'snippet': 'snippet'}
        ]

    def mock_download(url):
        time.sleep(0.1)
        return "This is a long enough text to pass the 500 char filter. " * 20

    mock_search.google_search.side_effect = mock_google_search
    mock_search.download_and_parse.side_effect = mock_download

    results = stage2_document_discovery(decomposition)

    # Verify order: Should follow the order of discovery (q1 results then q2 results)
    # Actually as_completed scrambles it.
    titles = [d['title'] for d in results]
    print(f"Result titles: {titles}")

    # Expected if ordered: Result q1... 1 Sub1, Result q1... 2 Sub1, Result q2... 1 Sub1, Result q2... 2 Sub1
    q1_full = 'q1 filetype:pdf OR site:.edu OR site:.org "research paper"'
    q2_full = 'q2 filetype:pdf OR site:.edu OR site:.org "research paper"'
    expected = [
        f'Result {q1_full} 1 Sub1',
        f'Result {q1_full} 2 Sub1',
        f'Result {q2_full} 1 Sub1',
        f'Result {q2_full} 2 Sub1'
    ]
    if titles == expected:
        print("✅ Discovery order preserved.")
    else:
        print(f"❌ Discovery order SCRAMBLED.")
        print(f"Actual: {titles}")
        print(f"Expected: {expected}")

if __name__ == "__main__":
    benchmark_stage4()
    test_order_preservation_stage3()
    test_order_preservation_stage2()
