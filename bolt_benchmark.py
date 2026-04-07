import time
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock dependencies
sys.modules['utils.search'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

import stages.stage4_scoring as stage4

def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5) # Simulate network/processing latency
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

class TestPerformance(unittest.TestCase):
    def test_stage4_parallelism(self):
        docs = [{"title": f"Doc {i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}} for i in range(6)]
        topic = "test topic"

        # We need to patch where it is used, which is stages.stage4_scoring.query_groq
        with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
            print("\nStarting Stage 4 Benchmark...")
            start_time = time.time()
            results = stage4.stage4_academic_scoring(docs, topic)
            end_time = time.time()

            duration = end_time - start_time
            print(f"Stage 4 duration with 6 docs: {duration:.2f}s")

            self.assertEqual(len(results), 6)

            # Verify order is preserved
            for i in range(6):
                self.assertEqual(results[i]['title'], f"Doc {i}")

            # If serial, it should take at least 6 * 0.5 = 3.0s
            # With 3 workers and 6 tasks, it should take 2 * 0.5 = 1.0s (+ overhead)
            self.assertLess(duration, 1.5, "Stage 4 should be parallelized and faster than serial execution.")

if __name__ == "__main__":
    unittest.main()
