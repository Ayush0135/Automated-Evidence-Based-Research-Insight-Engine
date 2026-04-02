import time
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import re

# Mock the modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Also mock utils.llm.query_gemini if needed by stage3
mock_llm.query_gemini = MagicMock()
mock_llm.query_stage = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring
from stages.stage3_analysis import stage3_document_analysis, analyze_single_document

def test_stage4_performance():
    print("\n--- Benchmarking Stage 4 ---")
    docs = [
        {'title': f'Doc {i}', 'analysis': {'research_problem': 'p', 'methodology': 'm', 'key_findings': 'f', 'novelty_assessment': 'n'}}
        for i in range(6)
    ]

    def mock_query_groq(prompt, **kwargs):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "s", "weaknesses": "w"}'

    mock_llm.query_groq.side_effect = mock_query_groq

    start_time = time.time()
    results = stage4_academic_scoring(docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 duration for 6 docs: {duration:.2f}s")

    # Check if order is preserved
    titles = [d['title'] for d in results]
    print(f"Order: {titles}")
    return duration

def test_stage3_order():
    print("\n--- Checking Stage 3 Chunk Order ---")
    # doc need to be long enough to trigger chunking (> 12000 chars)
    # 26000 chars should give 3 chunks of 12000 with 500 overlap
    doc = {
        'title': 'Test Doc',
        'raw_text': 'A' * 26000
    }

    last_prompt = ""

    def mock_query_gemini_capture(prompt, **kwargs):
        nonlocal last_prompt
        if "Analyze the following research document content" in prompt:
            last_prompt = prompt
            return '{"research_problem": "p"}'
        if "Analyze this segment" in prompt:
             match = re.search(r'Part (\d+)', prompt)
             part = match.group(1)
             # Artificial delay to cause out-of-order completion
             delay = 0.5 if part == '1' else 0.1
             time.sleep(delay)
             return f"Summary Part {part}"
        return '{"research_problem": "p"}'

    mock_llm.query_gemini.side_effect = mock_query_gemini_capture
    analyze_single_document(doc)

    print("Captured context in final prompt (summaries only):")
    summaries = re.findall(r'Summary Part \d+', last_prompt)
    print(summaries)

    # Sort them numerically based on the number in "Summary Part X"
    def sort_key(s):
        return int(re.search(r'\d+', s).group())

    if summaries == sorted(summaries, key=sort_key):
        print("Order preserved!")
    else:
        print("Order SCRAMBLED!")

if __name__ == "__main__":
    test_stage4_performance()
    test_stage3_order()
