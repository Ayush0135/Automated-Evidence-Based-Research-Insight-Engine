import sys
import os
import time
from unittest.mock import MagicMock

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

# Create mock modules
m_search = MagicMock()
m_llm = MagicMock()

# Setup sys.modules
sys.modules['utils.search'] = m_search
sys.modules['utils.llm'] = m_llm

# Now import the stages
import stages.stage3_analysis as stage3
import stages.stage4_scoring as stage4

def test_stage3_order():
    print("\n--- Testing Stage 3 Chunk Order ---")
    doc = {
        "title": "Big Doc",
        "raw_text": "A" * 20000 # Force chunking
    }

    call_prompts = []

    # Mock query_gemini to return the index of the chunk
    def mock_query(prompt, **kwargs):
        call_prompts.append(prompt)
        # Extract Part number from prompt
        import re
        match = re.search(r"Part (\d+)", prompt)
        if match:
            part = match.group(1)
            # Make part 1 slow to ensure part 2 would finish first if as_completed was used
            if part == "1":
                time.sleep(1)
            else:
                time.sleep(0.1)
            return f"SUMMARY_PART_{part}"
        return "SUMMARY_FINAL"

    m_llm.query_gemini.side_effect = mock_query

    result = stage3.analyze_single_document(doc)

    # Find the final analysis call prompt
    final_prompt = None
    for p in call_prompts:
        if "Analyze the following research document content" in p:
            final_prompt = p
            break

    if not final_prompt:
        print("FAIL: Could not find final analysis call.")
        return

    print("Final Analysis Context (summaries):")
    # Clean up the prompt to find summaries
    lines = final_prompt.split('\n')
    summaries = [line.strip() for line in lines if line.strip().startswith("SUMMARY_PART_")]
    print(summaries)

    expected = ["SUMMARY_PART_1", "SUMMARY_PART_2"]
    if summaries == expected:
        print("PASS: Chunk order preserved.")
    else:
        print(f"FAIL: Chunk order scrambled. Got: {summaries}")

def test_stage4_performance():
    print("\n--- Testing Stage 4 Performance and Order ---")
    docs = [{"title": f"Doc {i}", "analysis": {"research_problem": "P"}} for i in range(6)]
    topic = "AI"

    def slow_query(*args, **kwargs):
        time.sleep(1)
        return '{"score": 8, "strengths": "S", "weaknesses": "W"}'

    m_llm.query_groq.side_effect = slow_query

    start = time.time()
    results = stage4.stage4_academic_scoring(docs, topic)
    duration = time.time() - start

    print(f"\nTotal Duration: {duration:.2f}s")
    titles = [d['title'] for d in results]
    print(f"Titles: {titles}")

    expected_titles = [f"Doc {i}" for i in range(6)]
    if titles == expected_titles:
        print("PASS: Document order preserved.")
    else:
        print("FAIL: Document order SCRAMBLED.")

    # Expect ~6s if sequential, ~2s if parallel (6 docs / 3 workers)
    if duration < 3.0:
        print(f"PASS: Parallel execution detected (Speedup: {6/duration:.2f}x).")
    else:
        print(f"FAIL: Sequential execution detected or too slow (Duration: {duration:.2f}s).")

if __name__ == "__main__":
    test_stage3_order()
    test_stage4_performance()
