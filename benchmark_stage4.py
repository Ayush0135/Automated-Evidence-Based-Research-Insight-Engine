
import time
import sys
from unittest.mock import MagicMock

# Mocking dependencies
mock_llm = MagicMock()
mock_llm.query_groq = MagicMock(side_effect=lambda p, **kwargs: (time.sleep(1), '{"score": 8, "strengths": "good", "weaknesses": "none"}')[1])
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

def benchmark_scoring():
    docs = [{"title": f"Doc {i}", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}} for i in range(5)]
    topic = "Test Topic"

    print("Starting sequential scoring benchmark...")
    start_time = time.time()
    results = stage4_academic_scoring(docs, topic)
    end_time = time.time()

    print(f"Scored {len(results)} documents in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    benchmark_scoring()
