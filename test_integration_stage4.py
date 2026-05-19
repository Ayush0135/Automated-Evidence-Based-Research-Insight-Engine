
import sys
from unittest.mock import MagicMock

# Mock dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

import unittest
from unittest.mock import patch
from stages.stage4_scoring import stage4_academic_scoring

class TestStage4(unittest.TestCase):
    def test_order_preservation(self):
        # Create documents with specific titles to track order
        analyzed_documents = [
            {
                'title': f'Paper {i}',
                'analysis': {'research_problem': 'p', 'methodology': 'm', 'key_findings': 'f', 'novelty_assessment': 'n'}
            } for i in range(10)
        ]

        topic = "Test Topic"

        # Mock query_groq to return a score based on the title to verify correctness
        def mock_query_groq(prompt, **kwargs):
            # Extract paper number from prompt (it's in the title)
            import re
            match = re.search(r'Paper (\d+)', prompt)
            paper_num = match.group(1) if match else "0"
            return f'{{"score": {paper_num}, "strengths": "s", "weaknesses": "w"}}'

        with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
            results = stage4_academic_scoring(analyzed_documents, topic)

        # Verify order
        for i, result in enumerate(results):
            self.assertEqual(result['title'], f'Paper {i}')
            self.assertEqual(result['scoring']['score'], i)

    def test_missing_analysis_skips(self):
        analyzed_documents = [
            {'title': 'Good Paper', 'analysis': {'research_problem': 'p'}},
            {'title': 'Bad Paper'} # No analysis
        ]

        topic = "Test Topic"

        def mock_query_groq(prompt, **kwargs):
            return '{"score": 10, "strengths": "s", "weaknesses": "w"}'

        with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
            results = stage4_academic_scoring(analyzed_documents, topic)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Good Paper')

if __name__ == '__main__':
    unittest.main()
