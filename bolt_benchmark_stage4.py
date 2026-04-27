
import time
import sys
import os
from unittest.mock import MagicMock, patch

# Mocking internal modules before importing the stage
sys.modules['utils.llm'] = MagicMock()
sys.modules['utils.search'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5) # Simulate LLM delay
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

def main():
    docs = [{"title": f"Doc {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}} for i in range(10)]
    topic = "Test Topic"

    print("Running Stage 4 Sequential Benchmark...")
    start_time = time.time()
    with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
        results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    print(f"\nResults: {len(results)} documents scored.")
    print(f"Total time: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    main()
