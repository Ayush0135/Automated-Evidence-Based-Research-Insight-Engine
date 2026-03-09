
import sys
import time
import json
from unittest.mock import MagicMock

# Mocking the utils.llm and utils.search modules before they are imported by stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Mock implementations
def mock_query_groq(prompt, **kwargs):
    time.sleep(1) # Simulate network/inference delay
    return json.dumps({"score": 8, "strengths": "Strong", "weaknesses": "None"})

def mock_query_gemini(prompt, **kwargs):
    time.sleep(1) # Simulate network/inference delay
    if "Analyze this segment" in prompt:
        # Extract chunk index if possible for verification
        return f"Summary of chunk"
    return json.dumps({
        "research_problem": "Problem",
        "methodology": "Method",
        "key_findings": "Findings",
        "limitations": "Lim",
        "research_gaps": "Gap",
        "novelty_assessment": "Nov",
        "technical_depth_score": 8,
        "missing_entities": "None"
    })

mock_llm.query_groq = mock_query_groq
mock_llm.query_gemini = mock_query_gemini

# Now import the stages
from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import stage3_document_analysis

def test_stage4_performance():
    print("\n--- Testing Stage 4 Performance ---")
    docs = [
        {"title": f"Doc {i}", "url": f"http://test{i}.com", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]

    start_time = time.time()
    scored_docs = stage4_academic_scoring(docs, "Test Topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 duration for 6 docs: {duration:.2f}s")

    # Check order
    titles = [d['title'] for d in scored_docs]
    expected_titles = [f"Doc {i}" for i in range(6)]
    if titles == expected_titles:
        print("✅ Stage 4 order preserved.")
    else:
        print(f"❌ Stage 4 order SCRAMBLED: {titles}")

def test_stage3_ordering():
    print("\n--- Testing Stage 3 Ordering ---")
    # Small text for fast analysis, but we want to check chunk ordering
    large_text = "Chunk 1 content. " + "x" * 12000 + " Chunk 2 content. " + "y" * 12000 + " Chunk 3 content."
    docs = [
        {"title": "Large Doc", "raw_text": large_text}
    ]

    # We need to capture the order in which chunks are analyzed
    # Since we are mocking query_gemini, we can modify it to return the prompt part
    def mock_query_gemini_with_order(prompt, **kwargs):
        time.sleep(0.5)
        if "Analyze this segment (Part" in prompt:
            import re
            match = re.search(r'Part (\d+)', prompt)
            if match:
                return f"SUMMARY_PART_{match.group(1)}"
        return mock_query_gemini(prompt, **kwargs)

    mock_llm.query_gemini = mock_query_gemini_with_order

    analyzed_docs = stage3_document_analysis(docs)

    # In stage3, the chunk summaries are joined by \n
    # We can check if they are in order in the final prompt if we can intercept it,
    # or we can check the logic if we were to modify stage3 to store them.
    # For now, let's just see if it runs and check document order if we had multiple docs.

    docs_multi = [
        {"title": f"Doc {i}", "raw_text": f"Short text {i}"} for i in range(4)
    ]
    analyzed_multi = stage3_document_analysis(docs_multi)
    titles = [d['title'] for d in analyzed_multi]
    expected_titles = [f"Doc {i}" for i in range(4)]
    if titles == expected_titles:
        print("✅ Stage 3 document order preserved.")
    else:
        print(f"❌ Stage 3 document order SCRAMBLED: {titles}")

if __name__ == "__main__":
    test_stage4_performance()
    test_stage3_ordering()
