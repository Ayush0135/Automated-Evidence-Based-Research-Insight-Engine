
import time
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock the utils.llm module before importing stages
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

class TestStage4Performance(unittest.TestCase):
    def setUp(self):
        self.analyzed_docs = [
            {
                "title": f"Document {i}",
                "url": f"http://example.com/{i}",
                "analysis": {
                    "research_problem": "Problem X",
                    "methodology": "Method Y",
                    "key_findings": "Findings Z",
                    "novelty_assessment": "High"
                }
            } for i in range(6)
        ]
        self.topic = "Quantum Computing"

    def test_performance_and_order(self):
        # Mock query_groq to take 0.5 seconds per call
        def slow_query(*args, **kwargs):
            time.sleep(0.5)
            return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

        mock_llm.query_groq.side_effect = slow_query

        start_time = time.time()
        results = stage4_academic_scoring(self.analyzed_docs, self.topic)
        end_time = time.time()

        duration = end_time - start_time
        print(f"\nStage 4 took {duration:.2f} seconds for {len(self.analyzed_docs)} docs.")

        # Check order
        for i, doc in enumerate(results):
            self.assertEqual(doc['title'], f"Document {i}")

        self.assertEqual(len(results), 6)

if __name__ == "__main__":
    unittest.main()
