
import sys
from unittest.mock import MagicMock

# Comprehensive Mocking to prevent ModuleNotFoundError
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

# Mocking utils.llm after its dependencies are mocked
mock_llm = MagicMock()
mock_llm.query_groq = MagicMock(return_value='{"score": 9, "strengths": "excellent", "weaknesses": "minor"}')
sys.modules['utils.llm'] = mock_llm

from stages.stage4_scoring import stage4_academic_scoring

def test_integration():
    docs = [
        {"title": "Paper A", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}},
        {"title": "Paper B", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}
    ]
    topic = "AI Optimization"

    print("Running Stage 4 Integration Test...")
    results = stage4_academic_scoring(docs, topic)

    assert len(results) == 2
    assert results[0]['title'] == "Paper A"
    assert results[1]['title'] == "Paper B"
    assert 'scoring' in results[0]
    assert results[0]['scoring']['score'] == 9

    print("Stage 4 Integration Test Passed!")

if __name__ == "__main__":
    test_integration()
