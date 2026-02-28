import sys
import unittest
from unittest.mock import MagicMock
import time

# Mocking internal modules
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

class TestStage4Scoring(unittest.TestCase):
    def test_parallelization_and_order_preservation(self):
        # 1. Prepare mock data
        documents = [
            {'title': 'Paper 1', 'analysis': {'research_problem': 'p1', 'methodology': 'm1', 'key_findings': 'f1', 'novelty_assessment': 'n1'}},
            {'title': 'Paper 2', 'analysis': {'research_problem': 'p2', 'methodology': 'm2', 'key_findings': 'f2', 'novelty_assessment': 'n2'}},
            {'title': 'Paper 3', 'analysis': {'research_problem': 'p3', 'methodology': 'm3', 'key_findings': 'f3', 'novelty_assessment': 'n3'}},
            {'title': 'Paper 4', 'analysis': {'research_problem': 'p4', 'methodology': 'm4', 'key_findings': 'f4', 'novelty_assessment': 'n4'}},
            {'title': 'Paper 5', 'analysis': {'research_problem': 'p5', 'methodology': 'm5', 'key_findings': 'f5', 'novelty_assessment': 'n5'}}
        ]
        topic = "Quantum Computing"

        # 2. Define a side effect to simulate delay and verify concurrency
        # We want Paper 1 to take the longest, so if it wasn't concurrent,
        # it would block everything.
        # If order wasn't preserved by iterating over futures,
        # Paper 2 or 3 might appear first in the result list.
        def mock_query_groq(prompt, **kwargs):
            if "Paper 1" in prompt:
                time.sleep(1.0) # Slowest
                return '{"score": 9, "strengths": "s1", "weaknesses": "w1"}'
            elif "Paper 5" in prompt:
                time.sleep(0.1) # Fastest
                return '{"score": 5, "strengths": "s5", "weaknesses": "w5"}'
            else:
                time.sleep(0.5)
                # Extract paper number from prompt
                import re
                match = re.search(r'Paper (\d)', prompt)
                num = match.group(1) if match else "0"
                return f'{{"score": {num}, "strengths": "s{num}", "weaknesses": "w{num}"}}'

        mock_llm.query_groq.side_effect = mock_query_groq

        # 3. Run Stage 4
        start_time = time.time()
        scored_docs = stage4_academic_scoring(documents, topic)
        end_time = time.time()

        elapsed = end_time - start_time

        # 4. Assertions
        # Total expected time if serial: 1.0 + 0.5 + 0.5 + 0.5 + 0.1 = 2.6s
        # Total expected time if parallel (3 workers):
        # Round 1: Paper 1 (1s), Paper 2 (0.5s), Paper 3 (0.5s) -> Done in 1s
        # Round 2: Paper 4 (0.5s), Paper 5 (0.1s) -> Done in 0.5s
        # Total: ~1.5s
        print(f"\nElapsed time: {elapsed:.2f}s")
        self.assertLess(elapsed, 2.5, "Stage 4 should be parallelized (faster than serial).")

        # Verify order preservation
        self.assertEqual(len(scored_docs), 5)
        self.assertEqual(scored_docs[0]['title'], 'Paper 1')
        self.assertEqual(scored_docs[1]['title'], 'Paper 2')
        self.assertEqual(scored_docs[2]['title'], 'Paper 3')
        self.assertEqual(scored_docs[3]['title'], 'Paper 4')
        self.assertEqual(scored_docs[4]['title'], 'Paper 5')

        # Verify score data
        self.assertEqual(scored_docs[0]['scoring']['score'], 9)
        self.assertEqual(scored_docs[4]['scoring']['score'], 5)

if __name__ == '__main__':
    unittest.main()
