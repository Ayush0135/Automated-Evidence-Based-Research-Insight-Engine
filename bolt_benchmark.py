
import time
import sys
from unittest.mock import MagicMock

# Mocking internal dependencies to avoid API calls during benchmark
class MockLLM:
    def query_groq(self, prompt, json_mode=False, fallback_to_others=True):
        time.sleep(0.5) # Simulate LLM latency
        return '{"score": 8, "strengths": "Good paper", "weaknesses": "None"}'

    def query_gemini(self, prompt, fallback_to_others=True):
        return '["query 1", "query 2"]'

    def query_stage(self, stage, prompt):
        return '{"research_gap": "Gap", "proposed_contribution": "Contrib", "synthesis_of_related_work": "Synth", "methodology_plan": "Plan", "simulated_results_description": "Results", "conclusion_plan": "Conclusion"}'

mock_llm = MockLLM()
sys.modules['utils.llm'] = MagicMock()
sys.modules['utils.llm'].query_groq = mock_llm.query_groq
sys.modules['utils.llm'].query_gemini = mock_llm.query_gemini
sys.modules['utils.llm'].query_stage = mock_llm.query_stage

# Now import the stage to benchmark
from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    test_docs = [
        {"title": f"Paper {i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
        for i in range(6)
    ]

    print(f"Benchmarking Stage 4 with {len(test_docs)} documents...")
    start_time = time.time()
    results = stage4_academic_scoring(test_docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"Stage 4 Duration: {duration:.2f} seconds")

    # Check if order is preserved
    for i, doc in enumerate(results):
        if doc['title'] != f"Paper {i}":
             print(f"ERROR: Order mismatch at index {i}. Expected Paper {i}, got {doc['title']}")
             return
    print("Order preserved correctly.")
    return duration

if __name__ == "__main__":
    benchmark_stage4()
