import sys
import unittest
from unittest.mock import MagicMock, patch
import time

# Mock the entire utils.llm and utils.search before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Now import the stages
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

class TestPipelineParallelismAndOrder(unittest.TestCase):

    def setUp(self):
        # Reset mocks
        mock_llm.query_gemini.reset_mock()
        mock_llm.query_groq.reset_mock()
        mock_search.google_search.reset_mock()
        mock_search.download_and_parse.reset_mock()
        mock_search.google_search.side_effect = None
        mock_search.download_and_parse.side_effect = None

    def test_stage2_order_preservation(self):
        # Mock search results for multiple subtopics/queries
        def mock_google_search(query, num_results=6):
            if "Query A" in query:
                return [{'link': 'url_a1', 'title': 'Research Paper A1', 'snippet': 'Topic A snippet content'}]
            elif "Query B" in query:
                return [{'link': 'url_b1', 'title': 'Research Paper B1', 'snippet': 'Topic B snippet content'}]
            return []

        mock_search.google_search.side_effect = mock_google_search
        mock_search.download_and_parse.return_value = "This is a long enough text for a research paper mock." * 20

        decomp = {
            'subtopics': [
                {'name': 'Research Topic A', 'search_queries': ['Query A']},
                {'name': 'Research Topic B', 'search_queries': ['Query B']}
            ]
        }

        docs = stage2_document_discovery(decomp)

        # Verify order: url_a1 should come before url_b1 if order is preserved from subtopics
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]['url'], 'url_a1')
        self.assertEqual(docs[1]['url'], 'url_b1')

    def test_stage3_order_preservation(self):
        mock_llm.query_gemini.return_value = '{"research_problem": "test"}'

        docs = [
            {'title': 'Doc 1', 'raw_text': 'Some text for doc 1.'},
            {'title': 'Doc 2', 'raw_text': 'Some text for doc 2.'}
        ]

        analyzed_docs = stage3_document_analysis(docs)

        self.assertEqual(len(analyzed_docs), 2)
        self.assertEqual(analyzed_docs[0]['title'], 'Doc 1')
        self.assertEqual(analyzed_docs[1]['title'], 'Doc 2')

    def test_stage3_chunk_order_preservation(self):
        # Mock query_gemini to return different summaries for different chunks
        def mock_query_gemini(prompt, fallback_to_others=False):
            if "Part 1" in prompt: return "Summary 1"
            if "Part 2" in prompt: return "Summary 2"
            if "Analyze the following" in prompt: return '{"research_problem": "combined"}'
            return '{"research_problem": "default"}'

        mock_llm.query_gemini.side_effect = mock_query_gemini

        # Doc larger than 12000 chars to trigger chunking
        large_text = "A" * 15000 + "B" * 5000
        doc = {'title': 'Large Doc', 'raw_text': large_text}

        # Stage 3 uses query_gemini directly
        analyzed_docs = stage3_document_analysis([doc])

        # Check if combine prompt contains summaries in correct order
        # Need to find the "Analyze the following" call
        call_args_list = [call.args[0] for call in mock_llm.query_gemini.call_args_list]
        combine_prompt = [p for p in call_args_list if "Analyze the following" in p][0]

        self.assertIn("Summary 1\nSummary 2", combine_prompt)

    def test_stage4_parallel_and_order(self):
        # Simulate delay to test parallelism (conceptually)
        def mock_query_groq(prompt, json_mode=True, fallback_to_others=True):
            if "Doc 1" in prompt: time.sleep(0.1)
            return '{"score": 8, "strengths": "S", "weaknesses": "W"}'

        mock_llm.query_groq.side_effect = mock_query_groq

        docs = [
            {'title': 'Doc 1', 'analysis': {'research_problem': 'P1'}},
            {'title': 'Doc 2', 'analysis': {'research_problem': 'P2'}},
            {'title': 'Doc 3', 'analysis': {'research_problem': 'P3'}}
        ]

        scored_docs = stage4_academic_scoring(docs, "Topic")

        self.assertEqual(len(scored_docs), 3)
        # Verify order
        self.assertEqual(scored_docs[0]['title'], 'Doc 1')
        self.assertEqual(scored_docs[1]['title'], 'Doc 2')
        self.assertEqual(scored_docs[2]['title'], 'Doc 3')

        # Verify it actually scored them
        self.assertEqual(scored_docs[0]['scoring']['score'], 8)

if __name__ == '__main__':
    unittest.main()
