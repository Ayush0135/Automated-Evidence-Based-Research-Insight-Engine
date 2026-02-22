
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock internal modules before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Set up mock behaviors
mock_llm.query_gemini.return_value = "Mocked Gemini Response"
mock_llm.query_groq.return_value = '{"score": 8, "strengths": "Good", "weaknesses": "None"}'
mock_llm.query_stage.return_value = '{"mock": "data"}'

mock_search.google_search.return_value = [
    {'link': f'http://example.com/{i}', 'title': f'Doc {i}', 'snippet': f'Snippet {i}'} for i in range(1, 6)
]
# Ensure text is long enough to pass the 500 char filter
mock_search.download_and_parse.side_effect = lambda url: f"Full text content for {url} [research paper] " + "word " * 200

# Import stages after mocking
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

class TestPipelineOrdering(unittest.TestCase):

    def test_stage2_ordering(self):
        print("\nTesting Stage 2 Ordering...")
        decomposition = {
            'subtopics': [{'name': 'Academic Research', 'search_queries': ['query 1']}]
        }

        mock_search.google_search.return_value = [
            {'link': f'http://example.com/{i}', 'title': f'Academic Research {i}', 'snippet': f'Snippet {i}'} for i in range(1, 6)
        ]

        docs = stage2_document_discovery(decomposition)
        titles = [d['title'] for d in docs]
        print(f"Titles found: {titles}")
        self.assertEqual(len(titles), 5)
        # We expect [1, 2, 3, 4, 5] if order is preserved
        self.assertEqual(titles, [f'Academic Research {i}' for i in range(1, 6)])

    def test_stage3_ordering(self):
        print("\nTesting Stage 3 Ordering...")
        docs = [
            {'title': f'Doc {i}', 'raw_text': f'Content {i}', 'url': f'http://{i}'} for i in range(1, 6)
        ]

        # Mock analysis result to return different data for each doc
        def mock_query_gemini(prompt, **kwargs):
            if "Analyze the following research document" in prompt:
                import re
                match = re.search(r'Document Title: (Doc \d+)', prompt)
                title = match.group(1) if match else "Unknown"
                return f'{{"research_problem": "Problem for {title}", "methodology": "M", "key_findings": "F", "limitations": "L", "research_gaps": "G", "novelty_assessment": "N", "technical_depth_score": 8, "missing_entities": "E"}}'
            return "Summary"

        mock_llm.query_gemini.side_effect = mock_query_gemini

        analyzed = stage3_document_analysis(docs)
        titles = [d['title'] for d in analyzed]
        print(f"Titles analyzed: {titles}")
        self.assertEqual(titles, [f'Doc {i}' for i in range(1, 6)])

    def test_stage4_ordering(self):
        print("\nTesting Stage 4 Ordering...")
        docs = [
            {'title': f'Doc {i}', 'analysis': {'research_problem': 'P'}, 'url': f'http://{i}'} for i in range(1, 6)
        ]

        scored = stage4_academic_scoring(docs, "topic")
        titles = [d['title'] for d in scored]
        print(f"Titles scored: {titles}")
        self.assertEqual(titles, [f'Doc {i}' for i in range(1, 6)])

if __name__ == '__main__':
    unittest.main()
