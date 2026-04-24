
import time
import sys
import unittest.mock as mock

# Define the mock function
def mock_query_groq(prompt, json_mode=False, fallback_to_others=True):
    time.sleep(0.5) # Simulate LLM delay
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

# Create the mock object
mock_llm_mod = mock.MagicMock()
mock_llm_mod.query_groq.side_effect = mock_query_groq

# Inject the mock into sys.modules
sys.modules['utils.llm'] = mock_llm_mod

# Now import stage4
from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    test_docs = [
        {
            "title": f"Doc {i}",
            "analysis": {
                "research_problem": "Problem",
                "methodology": "Method",
                "key_findings": "Findings",
                "novelty_assessment": "Novelty"
            }
        } for i in range(10)
    ]

    print(f"Benchmarking Stage 4 with {len(test_docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(test_docs, "Test Topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 took {duration:.2f} seconds.")
    return duration

if __name__ == "__main__":
    benchmark_stage4()
