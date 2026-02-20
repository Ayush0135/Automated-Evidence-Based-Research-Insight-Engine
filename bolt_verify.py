import sys
import unittest
from unittest.mock import MagicMock, patch

# Mocking utils before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Mock functions for LLM
def mock_query_groq(prompt, **kwargs):
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

def mock_query_gemini(prompt, **kwargs):
    return '{"research_problem": "test", "methodology": "test", "key_findings": "test", "limitations": "test", "research_gaps": "test", "novelty_assessment": "test", "technical_depth_score": 5, "missing_entities": "none"}'

mock_llm.query_groq.side_effect = mock_query_groq
mock_llm.query_gemini.side_effect = mock_query_gemini

# Mock functions for Search
def mock_google_search(query, **kwargs):
    # Return results that match keywords in the title/snippet for 'Quantum' subtopic
    return [{'link': f'http://test{i}.com', 'title': f'Quantum paper {i}', 'snippet': f'Snippet about Quantum {i}'} for i in range(3)]

def mock_download_and_parse(url):
    return "This is a long enough text to pass the 500 character limit. " * 20

mock_search.google_search.side_effect = mock_google_search
mock_search.download_and_parse.side_effect = mock_download_and_parse

# Now import stages
from stages.stage4_scoring import stage4_academic_scoring
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis

class TestBoltOptimizations(unittest.TestCase):
    def test_stage4_parallelism_and_order(self):
        print("\nVerifying Stage 4 Order Preservation...")
        docs = [
            {'title': 'Doc 1', 'analysis': {'research_problem': 'p1'}},
            {'title': 'Doc 2', 'analysis': {'research_problem': 'p2'}},
            {'title': 'Doc 3', 'analysis': {'research_problem': 'p3'}}
        ]
        topic = "Quantum Computing"

        scored = stage4_academic_scoring(docs, topic)

        self.assertEqual(len(scored), 3)
        self.assertEqual(scored[0]['title'], 'Doc 1')
        self.assertEqual(scored[1]['title'], 'Doc 2')
        self.assertEqual(scored[2]['title'], 'Doc 3')
        print("Stage 4 Order Verified.")

    def test_stage2_order(self):
        print("\nVerifying Stage 2 Order Preservation...")
        decomposition = {
            'subtopics': [
                {'name': 'Quantum', 'search_queries': ['q1', 'q2']}
            ]
        }
        docs = stage2_document_discovery(decomposition)
        self.assertTrue(len(docs) > 0)
        # Check that titles appear in expected order (from query q1 then q2)
        # Query q1 returns papers 0, 1, 2. Query q2 returns papers 0, 1, 2 (but filtered by seen_urls)
        # So we expect papers 0, 1, 2 in that order.
        self.assertEqual(docs[0]['title'], 'Quantum paper 0')
        self.assertEqual(docs[1]['title'], 'Quantum paper 1')
        self.assertEqual(docs[2]['title'], 'Quantum paper 2')
        print("Stage 2 Order Verified.")

    def test_stage3_order(self):
        print("\nVerifying Stage 3 Order Preservation...")
        docs = [
            {'title': 'Doc 1', 'raw_text': "Short text " * 50},
            {'title': 'Doc 2', 'raw_text': "Long text " * 2000} # Trigger chunking
        ]
        analyzed = stage3_document_analysis(docs)
        self.assertEqual(len(analyzed), 2)
        self.assertEqual(analyzed[0]['title'], 'Doc 1')
        self.assertEqual(analyzed[1]['title'], 'Doc 2')
        print("Stage 3 Order Verified.")

if __name__ == '__main__':
    unittest.main()
