import sys
import time
import unittest
from unittest.mock import MagicMock

# Create a mock for the module
mock_llm_module = MagicMock()
mock_search_module = MagicMock()

# Mock query_groq to take 0.3s per call and return valid JSON
def mock_query(*args, **kwargs):
    time.sleep(0.3)
    return '{"score": 8, "strengths": "none", "weaknesses": "none"}'

mock_llm_module.query_groq = mock_query

# Inject mocks into sys.modules
sys.modules['utils.llm'] = mock_llm_module
sys.modules['utils.search'] = mock_search_module

# Now import the stage to test
from stages.stage4_scoring import stage4_academic_scoring

class TestStage4Performance(unittest.TestCase):
    def setUp(self):
        self.docs = [
            {
                'title': f'Doc {i}',
                'analysis': {
                    'research_problem': 'prob',
                    'methodology': 'meth',
                    'key_findings': 'find',
                    'novelty_assessment': 'nov'
                }
            } for i in range(12)
        ]
        self.topic = "test topic"

    def test_stage4_parallel_speed_and_order(self):
        # 12 docs, 0.3s each. Sequential would take 3.6s.
        # With 3 workers, it should take ~1.2s + overhead.
        start_time = time.time()
        results = stage4_academic_scoring(self.docs, self.topic)
        end_time = time.time()

        duration = end_time - start_time
        print(f"\nParallel Stage 4 took: {duration:.2f}s")

        # Performance check: Should be under 1.5s (allowing some overhead)
        self.assertLess(duration, 2.0, f"Parallel execution too slow: {duration:.2f}s")
        self.assertEqual(len(results), 12)

        # Verify order preservation
        for i, doc in enumerate(results):
            self.assertEqual(doc['title'], f'Doc {i}', f"Order mismatch at index {i}")

if __name__ == '__main__':
    unittest.main()
