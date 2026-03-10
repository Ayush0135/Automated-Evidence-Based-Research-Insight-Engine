import time
import sys
import os
from unittest.mock import MagicMock, patch

# Mocking internal modules to avoid API calls and missing dependencies
mock_llm = MagicMock()
mock_search = MagicMock()

# Mock query_gemini to return predictable results for ordering check
def mock_query_gemini(prompt, **kwargs):
    if "Analyze this segment (Part" in prompt:
        # Extract part number to verify order
        import re
        match = re.search(r"Part (\d+)", prompt)
        if match:
            return f"Summary of Part {match.group(1)}"
    return '{"research_problem": "mock", "methodology": "mock", "key_findings": "mock", "limitations": "mock", "research_gaps": "mock", "novelty_assessment": "mock", "technical_depth_score": 5, "missing_entities": "mock"}'

mock_llm.query_gemini = mock_query_gemini

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5) # Simulate API latency
    return '{"score": 8, "strengths": "mock", "weaknesses": "mock"}'

mock_llm.query_groq = mock_query_groq
mock_llm.query_stage = MagicMock(return_value='{"mock": "json"}')

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Now import the stages
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def verify_stage3_ordering():
    print("\n--- Verifying Stage 3 Chunk Ordering ---")
    # Large document (>12000 chars) to trigger chunking
    doc = {
        "title": "Test Doc",
        "raw_text": "A" * 15000,
        "url": "http://test.com"
    }

    analyzed_docs = stage3_document_analysis([doc])

    # In stage3_analysis.py, chunk_summaries are joined by "\n"
    # and passed to the final prompt. We need to check if they are in order.
    # Actually, we should check the internal state if possible, but stage3 doesn't return it.
    # Let's modify stage3 later to use ordered iteration.
    print("Stage 3 analysis completed.")

def verify_stage4_performance():
    print("\n--- Measuring Stage 4 Performance ---")
    docs = []
    for i in range(6):
        docs.append({
            "title": f"Doc {i}",
            "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}
        })

    start_time = time.time()
    scored_docs = stage4_academic_scoring(docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 took {duration:.2f} seconds for {len(docs)} documents.")

    # Check ordering
    for i, doc in enumerate(scored_docs):
        if doc['title'] != f"Doc {i}":
            print(f"ORDERING FAILED: Expected Doc {i}, got {doc['title']}")
            return False

    print("Ordering preserved in Stage 4.")
    return duration

if __name__ == "__main__":
    verify_stage3_ordering()
    verify_stage4_performance()
