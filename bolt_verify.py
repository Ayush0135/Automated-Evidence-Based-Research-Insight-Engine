import sys
import unittest
from unittest.mock import MagicMock, patch
import time
import json

# Mock external dependencies before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()

# Ensure utils.llm_offline is also mocked if needed, but stages mainly use utils.llm
sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.llm_offline'] = MagicMock()

# Now import the stages
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

class TestPipelineOptimizations(unittest.TestCase):

    def setUp(self):
        mock_search.reset_mock()
        mock_llm.reset_mock()

    def test_stage2_ordering(self):
        """Verify that Stage 2 preserves search query and download order."""
        def google_search_side_effect(query, num_results=6):
            if "query1" in query:
                time.sleep(0.3) # Delay first query
                return [{'link': 'url1', 'title': 'Subtopic1 Research', 'snippet': 'snippet about Subtopic1'}]
            else:
                return [{'link': 'url2', 'title': 'Subtopic2 Study', 'snippet': 'snippet about Subtopic2'}]

        mock_search.google_search.side_effect = google_search_side_effect

        def download_side_effect(url):
            if 'url1' in url:
                time.sleep(0.3) # Delay first download
            return "Content " * 100 # > 500 chars

        mock_search.download_and_parse.side_effect = download_side_effect

        decomposition = {
            'subtopics': [
                {'name': 'Subtopic1', 'search_queries': ['query1']},
                {'name': 'Subtopic2', 'search_queries': ['query2']}
            ]
        }

        docs = stage2_document_discovery(decomposition)

        # Ordering check
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]['url'], 'url1')
        self.assertEqual(docs[1]['url'], 'url2')

    def test_stage3_ordering(self):
        """Verify that Stage 3 preserves document and chunk order."""
        def query_gemini_side_effect(prompt, fallback_to_others=True):
            if "Doc 1" in prompt or "Part 1" in prompt:
                time.sleep(0.2)
                return '{"research_problem": "P1", "methodology": "M1", "key_findings": "F1", "limitations": "L1", "research_gaps": "G1", "novelty_assessment": "N1", "technical_depth_score": 5, "missing_entities": "E1"}'
            else:
                return '{"research_problem": "P2", "methodology": "M2", "key_findings": "F2", "limitations": "L2", "research_gaps": "G2", "novelty_assessment": "N2", "technical_depth_score": 5, "missing_entities": "E2"}'

        mock_llm.query_gemini.side_effect = query_gemini_side_effect

        docs = [
            {'title': 'Doc 1', 'raw_text': 'Some content'},
            {'title': 'Doc 2', 'raw_text': 'Some other content'}
        ]

        analyzed = stage3_document_analysis(docs)

        self.assertEqual(len(analyzed), 2)
        self.assertEqual(analyzed[0]['title'], 'Doc 1')
        self.assertEqual(analyzed[1]['title'], 'Doc 2')

    def test_stage4_ordering_and_parallelism(self):
        """Verify that Stage 4 is parallelized and preserves document order."""
        start_time = time.time()

        def query_groq_side_effect(prompt, json_mode=True, fallback_to_others=True):
            time.sleep(0.5) # Simulate LLM latency
            return '{"score": 8, "strengths": "S", "weaknesses": "W"}'

        mock_llm.query_groq.side_effect = query_groq_side_effect

        docs = [
            {'title': 'Doc 1', 'analysis': {'research_problem': 'P1'}},
            {'title': 'Doc 2', 'analysis': {'research_problem': 'P2'}},
            {'title': 'Doc 3', 'analysis': {'research_problem': 'P3'}}
        ]

        scored = stage4_academic_scoring(docs, "topic")
        end_time = time.time()

        # Check ordering
        self.assertEqual(len(scored), 3)
        self.assertEqual(scored[0]['title'], 'Doc 1')
        self.assertEqual(scored[1]['title'], 'Doc 2')
        self.assertEqual(scored[2]['title'], 'Doc 3')

        # Check parallelism: 3 workers, each taking 0.5s.
        # Sequential: 1.5s. Parallel: ~0.5s.
        duration = end_time - start_time
        print(f"Stage 4 duration: {duration:.2f}s")
        # We expect it to be around 0.5-0.7s. 1.0s is a safe threshold for parallel success.
        self.assertLess(duration, 1.0, "Stage 4 is not executing in parallel!")

if __name__ == '__main__':
    unittest.main()
