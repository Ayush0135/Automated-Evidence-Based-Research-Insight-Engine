
import sys
from unittest.mock import MagicMock, patch

# Mock all external dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

from stages.stage4_scoring import stage4_academic_scoring

def test_stage4_integration():
    print("Running Stage 4 Integration Test...")
    topic = "Test Topic"
    documents = [
        {"title": "Doc 1", "analysis": {"research_problem": "p1"}},
        {"title": "Doc 2", "analysis": {"research_problem": "p2"}}
    ]

    mock_response = '{"score": 9, "strengths": "s", "weaknesses": "w"}'

    with patch('stages.stage4_scoring.query_groq', return_value=mock_response):
        results = stage4_academic_scoring(documents, topic)

    assert len(results) == 2
    assert results[0]['scoring']['score'] == 9
    assert results[1]['scoring']['score'] == 9
    assert results[0]['title'] == "Doc 1"
    assert results[1]['title'] == "Doc 2"

    print("Stage 4 Integration Test PASSED")

if __name__ == "__main__":
    test_stage4_integration()
