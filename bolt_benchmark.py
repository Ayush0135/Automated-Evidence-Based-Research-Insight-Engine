import time
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock internal modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Mock query_groq with a delay to simulate LLM latency
def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5) # 500ms delay per call
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

mock_llm.query_groq.side_effect = mock_query_groq
mock_llm.query_gemini.return_value = "Mocked Response"

# Now import the stages
from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import chunk_text, stage3_document_analysis

def benchmark_stage4():
    print("Benchmarking Stage 4 (Academic Scoring)...")

    mock_docs = [
        {"title": f"Doc {i}", "url": f"http://test{i}.com", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]

    start_time = time.time()
    results = stage4_academic_scoring(mock_docs, "Test Topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 completed in {duration:.2f} seconds.")

    # Check order
    order_correct = all(results[i]['title'] == f"Doc {i}" for i in range(len(results)))
    print(f"Order preserved: {order_correct}")

    return duration, order_correct

def verify_stage3_order():
    print("\nVerifying Stage 3 (Document Analysis) chunk order...")
    # Mock query_gemini to return its index
    def mock_query_gemini_with_index(prompt, **kwargs):
        if "Part" in prompt:
            import re
            match = re.search(r'Part (\d+)', prompt)
            if match:
                return f"Summary of Part {match.group(1)}"
        return "Generic Summary"

    mock_llm.query_gemini.side_effect = mock_query_gemini_with_index

    # Large document that will be chunked
    large_text = "A" * 26000 # Will result in 3 chunks with default settings (12000 size, 500 overlap)
    # chunk 1: 0-12000
    # chunk 2: 11500-23500
    # chunk 3: 23000-26000

    mock_doc = {
        "title": "Large Doc",
        "url": "http://large.com",
        "raw_text": large_text
    }

    # We need to call stage3_document_analysis
    # It has max_workers=2 for docs, and max_workers=3 for chunks
    results = stage3_document_analysis([mock_doc])

    if results and 'analysis' in results[0]:
        # The logic in stage3_document_analysis for large docs:
        # text_context = "\n".join(chunk_summaries)
        # We can't directly see chunk_summaries, but we can see the final prompt if we mock it better
        # or we can check if stage3_document_analysis preserved order if we modify it to return summaries
        pass

    print("Stage 3 verification logic completed (manual check of code required until fix applied).")

if __name__ == "__main__":
    duration, order = benchmark_stage4()
    # verify_stage3_order()

    # Initial run (sequential): 6 docs * 0.5s = 3.0s expected
    if duration > 2.5:
        print("\nRESULT: Stage 4 is running SEQUENTIALLY.")
    else:
        print(f"\nRESULT: Stage 4 is running PARALLEL (Duration: {duration:.2f}s).")
