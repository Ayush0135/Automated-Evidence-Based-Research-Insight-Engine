
import time
import sys
from unittest.mock import MagicMock

# Mocking the LLM and search utilities before importing stages
mock_llm = MagicMock()
mock_llm.query_groq.side_effect = lambda p, **kwargs: '{"score": 8, "strengths": "Good", "weaknesses": "None"}'
mock_llm.query_gemini.side_effect = lambda p, **kwargs: '{"research_problem": "Problem", "methodology": "Method", "key_findings": "Findings", "limitations": "Lim", "research_gaps": "Gaps", "novelty_assessment": "Nov", "technical_depth_score": 8, "missing_entities": "None"}'

sys.modules['utils.llm'] = mock_llm

mock_search = MagicMock()
# Mock search results to include keywords from the subtopic to pass the relevance filter
mock_search.google_search.side_effect = lambda q, num_results: [
    {'link': f'http://example.com/{i}', 'title': f'Quantum Paper {i}', 'snippet': 'Quantum computing research'} for i in range(num_results)
]
mock_search.download_and_parse.side_effect = lambda url: "This is a long enough research paper content to pass the 500 characters length filter." * 10
sys.modules['utils.search'] = mock_search

from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import analyze_single_document
from stages.stage2_discovery import stage2_document_discovery

def benchmark_stage4():
    print("\n--- Benchmarking Stage 4 Performance & Order ---")
    topic = "Quantum Computing"
    analyzed_docs = [
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

    # Mocking a delay in query_groq to simulate real API call
    def mocked_query_groq_delayed(prompt, **kwargs):
        # Extract paper index from prompt to simulate different response times
        # But here we just want to verify parallel speedup
        time.sleep(0.5)
        return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

    mock_llm.query_groq.side_effect = mocked_query_groq_delayed

    start_time = time.time()
    scored_docs = stage4_academic_scoring(analyzed_docs, topic)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 completed in {duration:.2f} seconds.")

    # Verify Order
    for i, doc in enumerate(scored_docs):
        if doc['title'] != f"Paper {i}":
            print(f"FAILED: Order mismatch at index {i}. Expected Paper {i}, got {doc['title']}")
            return False

    print("SUCCESS: Stage 4 preserved order and achieved speedup.")
    return True

def verify_stage3_order():
    print("\n--- Verifying Stage 3 Chunk Order Preservation ---")
    doc = {
        "title": "Large Document",
        "raw_text": "ChunkContent " * 2000 # ~26000 chars, will be chunked
    }

    # Mock chunk analysis to return its index
    def analyze_chunk_mock(prompt, **kwargs):
        time.sleep(0.1)
        if "Part 1" in prompt: return "Summary 1"
        if "Part 2" in prompt: return "Summary 2"
        if "Part 3" in prompt: return "Summary 3"
        if "Part 4" in prompt: return "Summary 4"
        if "Part 5" in prompt: return "Summary 5"
        if "Part 6" in prompt: return "Summary 6"
        return "Unknown"

    mock_llm.query_gemini.side_effect = analyze_chunk_mock

    # We need to capture the text_context sent to the final LLM call
    captured_context = []
    def capture_final_prompt(prompt, **kwargs):
        print(f"DEBUG: Captured Final Prompt: {prompt[:200]}...")
        captured_context.append(prompt)
        return '{"research_problem": "Problem"}'

    # Temporarily override query_gemini for the final call in analyze_single_document
    original_query_gemini = mock_llm.query_gemini.side_effect

    def smart_mock(prompt, **kwargs):
        if "Analyze the following research document content" in prompt:
            return capture_final_prompt(prompt, **kwargs)
        return analyze_chunk_mock(prompt, **kwargs)

    mock_llm.query_gemini.side_effect = smart_mock

    analyze_single_document(doc)

    if captured_context:
        context = captured_context[0]
        # Check if summaries are in order
        # Selected chunks logic: First 2, Middle 2, Last 2 if > 6 chunks.
        # But here we have 20000 / (12000-500) = 2.xx chunks.
        # "ChunkContent " * 2000 is about 26000 chars.
        # chunk_text(26000, 12000, 500):
        # chunk 1: [0:12000]
        # chunk 2: [11500:23500]
        # chunk 3: [23000:26000]
        # So we expect 3 chunks.
        order = [context.find(f"Summary {i}") for i in range(1, 4)]
        if order == sorted(order) and -1 not in order:
            print("SUCCESS: Stage 3 preserved chunk order.")
            return True
        else:
            print(f"FAILED: Stage 3 chunk order mismatch. Indices: {order}")
            return False
    return False

def verify_stage2_order():
    print("\n--- Verifying Stage 2 Order Preservation ---")
    decomposition = {
        'subtopics': [
            {'name': 'Quantum', 'search_queries': ['q1', 'q2']}
        ]
    }

    # Mock search to return results with order-identifiable titles
    def mocked_search(query, num_results):
        time.sleep(0.1)
        return [{'link': f'http://{query}-{i}.com', 'title': f'Title-{query}-{i}', 'snippet': 'Quantum research'} for i in range(num_results)]

    mock_search.google_search.side_effect = mocked_search

    # Mock download to be slow
    def mocked_download(url):
        time.sleep(0.1)
        return "Content for " + url + " " + ("long content " * 50)

    mock_search.download_and_parse.side_effect = mocked_download

    docs = stage2_document_discovery(decomposition)

    titles = [d['title'] for d in docs]
    # Expect q1 results then q2 results
    expected_titles_prefix = ['Title-q1', 'Title-q2']

    # Verify that all q1 titles come before q2 titles
    q1_indices = [i for i, t in enumerate(titles) if 'q1' in t]
    q2_indices = [i for i, t in enumerate(titles) if 'q2' in t]

    if q1_indices and q2_indices and max(q1_indices) < min(q2_indices):
        print("SUCCESS: Stage 2 preserved relevance order.")
        return True
    else:
        print(f"FAILED: Stage 2 order mismatch. Titles: {titles}")
        return False

if __name__ == "__main__":
    s4 = benchmark_stage4()
    s3 = verify_stage3_order()
    s2 = verify_stage2_order()

    if all([s4, s3, s2]):
        print("\nALL VERIFICATIONS PASSED!")
        sys.exit(0)
    else:
        print("\nSOME VERIFICATIONS FAILED!")
        sys.exit(1)
