import sys
from unittest.mock import MagicMock, patch

# Mock all dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_preserves_order():
    docs = [
        {'title': 'Doc A', 'analysis': {'key': 'val'}},
        {'title': 'Doc B', 'analysis': {'key': 'val'}},
        {'title': 'Doc C', 'analysis': {'key': 'val'}},
    ]
    topic = "Topic"

    # Mock query_groq to return different scores but we mostly care about titles
    with patch('stages.stage4_scoring.query_groq') as mock_query:
        mock_query.side_effect = [
            '{"score": 9}',
            '{"score": 8}',
            '{"score": 7}'
        ]

        results = stage4_academic_scoring(docs, topic)

        assert len(results) == 3
        assert results[0]['title'] == 'Doc A'
        assert results[1]['title'] == 'Doc B'
        assert results[2]['title'] == 'Doc C'
        print("Integration test passed: Order preserved and all docs processed.")

if __name__ == "__main__":
    try:
        test_stage4_preserves_order()
    except Exception as e:
        print(f"Integration test failed: {e}")
        sys.exit(1)
