
import time
import sys
from unittest.mock import MagicMock, patch

# Mock dependencies for stage4
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()

import stages.stage4_scoring as stage4

def mock_query_groq(prompt, **kwargs):
    # Simulate LLM delay
    time.sleep(1)
    return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

@patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq)
def test_integration_stage4(mock_query):
    docs = [
        {'title': f'Doc {i}', 'analysis': {'research_problem': 'P', 'methodology': 'M', 'key_findings': 'F', 'novelty_assessment': 'N'}}
        for i in range(5)
    ]

    print(f"Testing Stage 4 Parallel Scoring with {len(docs)} documents...")
    scored_docs = stage4.stage4_academic_scoring(docs, "test topic")

    assert len(scored_docs) == 5
    for doc in scored_docs:
        assert 'scoring' in doc
        assert doc['scoring']['score'] == 8

    print("Stage 4 Integration Test [OK]")

if __name__ == '__main__':
    test_integration_stage4()
