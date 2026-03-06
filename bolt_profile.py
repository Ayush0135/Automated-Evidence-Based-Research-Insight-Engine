
import time
import sys
import os
from unittest.mock import MagicMock, patch

# Mock the entire utils modules to avoid real API calls
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

def mock_query_groq(prompt, **kwargs):
    time.sleep(1)  # Simulate 1s latency
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

def mock_query_gemini(prompt, **kwargs):
    if "Analyze this segment" in prompt:
        import re
        match = re.search(r'Part (\d+)', prompt)
        idx = int(match.group(1)) if match else 0
        # Wait longer for earlier chunks to force them to complete later
        # Chunk 1 (idx 0): 0.5s
        # Chunk 2 (idx 1): 0.25s
        # Chunk 3 (idx 2): 0.16s
        time.sleep(0.5 / (idx + 1))
        return f"Summary of chunk {idx}"
    else:
        time.sleep(1)
        return '{"research_problem": "Problem", "methodology": "Method", "key_findings": "Findings"}'

mock_llm.query_groq = mock_query_groq
mock_llm.query_gemini = mock_query_gemini

# Now import the stages
from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import stage3_document_analysis

def profile_stage4():
    print("\nProfiling Stage 4 (Sequential)...")
    docs = [{"title": f"Doc {i}", "analysis": {"key": "val"}} for i in range(3)]
    start = time.time()
    results = stage4_academic_scoring(docs, "Topic")
    end = time.time()
    duration = end - start
    print(f"Stage 4 duration for 3 docs: {duration:.2f}s (Expected ~3s for sequential)")
    return duration

def verify_stage3_order():
    print("\nVerifying Stage 3 Chunk Order...")
    # Large doc to trigger chunking
    doc = {
        "title": "Large Doc",
        "raw_text": "A" * 20000 # > 12000 triggers chunking
    }

    # Patch query_gemini directly in the module it was imported into
    with patch('stages.stage3_analysis.query_gemini', side_effect=mock_query_gemini):
        # We need to capture the text_context in analyze_single_document
        # I'll patch the final query_gemini call to see the prompt it receives

        with patch('stages.stage3_analysis.query_gemini') as mock_final_query:
            mock_final_query.side_effect = mock_query_gemini
            stage3_document_analysis([doc])

            # Get the prompt from the last call
            last_call = mock_final_query.call_args_list[-1]
            prompt = last_call[0][0]

            # Check for chunk order in the prompt
            print("Captured prompt context section:")
            # Find the section after 'Content/Context:'
            if "Content/Context:" in prompt:
                context_part = prompt.split("Content/Context:")[1].split("Task:")[0].strip()
                print(context_part)

                # If it's using as_completed, it might be out of order.
                # Since chunk 2 (idx 1) and 3 (idx 2) are faster than chunk 1 (idx 0)
                # it's likely to be out of order if as_completed is used.

if __name__ == "__main__":
    profile_stage4()
    verify_stage3_order()
