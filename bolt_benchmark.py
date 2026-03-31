
import time
import sys
from unittest.mock import MagicMock, patch

# Mocking external dependencies before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Now import stages
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    print("\n>>> Benchmarking Stage 4: Academic Scoring")
    docs = [
        {"title": f"Doc {i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]

    def mock_query_groq(prompt, **kwargs):
        time.sleep(0.5) # Simulate LLM delay
        # Extract Doc index from prompt to return it in the mock response for order verification
        for i in range(6):
            if f"Doc {i}" in prompt:
                return f'{{"score": {i}, "strengths": "S", "weaknesses": "W"}}'
        return '{"score": 0, "strengths": "S", "weaknesses": "W"}'

    mock_llm.query_groq.side_effect = mock_query_groq

    start_time = time.time()
    results = stage4_academic_scoring(docs, "Topic")
    duration = time.time() - start_time

    print(f"Stage 4 duration: {duration:.2f}s")

    order_correct = all(results[i]['scoring']['score'] == i for i in range(len(results)))
    print(f"Order preserved: {order_correct}")
    return duration, order_correct

def benchmark_stage2():
    print("\n>>> Benchmarking Stage 2: Document Discovery")
    decomposition = {
        'subtopics': [
            {'name': 'Topic A', 'search_queries': ['query A1', 'query A2']}
        ]
    }

    def mock_google_search(query, **kwargs):
        # Return results that identify the query index
        idx = 1 if 'A1' in query else 2
        return [{'link': f'http://{idx}.com', 'title': f'Result {idx}', 'snippet': 'Topic A'}]

    def mock_download(url):
        time.sleep(0.2)
        return "Relevant content for Topic A " * 50

    mock_search.google_search.side_effect = mock_google_search
    mock_search.download_and_parse.side_effect = mock_download

    results = stage2_document_discovery(decomposition)

    # Check if Result 1 comes before Result 2 (based on query submission order)
    # Note: stage2 currently uses as_completed, so this might be random/wrong
    titles = [r['title'] for r in results]
    print(f"Results order: {titles}")
    order_correct = titles == ['Result 1', 'Result 2']
    print(f"Order preserved: {order_correct}")
    return order_correct

def benchmark_stage3():
    print("\n>>> Benchmarking Stage 3: Document Analysis")
    # 2 documents, one large (for chunking)
    docs = [
        {"title": "Doc 0", "raw_text": "Short text"},
        {"title": "Doc 1", "raw_text": "Long text " * 2000} # > 12000 chars
    ]

    def mock_query_gemini(prompt, **kwargs):
        time.sleep(0.3)
        if "Segment" in prompt:
            # Chunk analysis
            for i in range(10):
                if f"Part {i+1}" in prompt:
                    return f"Summary {i+1}"
        else:
            # Full doc analysis
            for i in range(2):
                if f"Doc {i}" in prompt:
                    return f'{{"research_problem": "P{i}", "methodology": "M", "key_findings": "F", "novelty_assessment": "N", "technical_depth_score": 5, "missing_entities": "E"}}'
        return "{}"

    mock_llm.query_gemini.side_effect = mock_query_gemini

    results = stage3_document_analysis(docs)

    # Check document order
    titles = [r['title'] for r in results]
    print(f"Document order: {titles}")
    doc_order_correct = titles == ["Doc 0", "Doc 1"]

    # Check chunk order for Doc 1
    doc1 = next(r for r in results if r['title'] == "Doc 1")
    # The prompt for final analysis of Doc 1 contains joined chunk summaries
    # We can't easily check the internal `text_context` without mocking more,
    # but we can check if it eventually works.

    print(f"Doc order preserved: {doc_order_correct}")
    return doc_order_correct

if __name__ == "__main__":
    benchmark_stage2()
    benchmark_stage3()
    benchmark_stage4()
