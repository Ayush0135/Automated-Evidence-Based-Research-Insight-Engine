
import sys
from unittest.mock import MagicMock

# Mock dependencies that are missing or cause issues
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

import time
from unittest.mock import patch
from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4():
    # Mocking analyzed_documents
    analyzed_documents = [
        {
            'title': f'Paper {i}',
            'analysis': {
                'research_problem': 'problem',
                'methodology': 'method',
                'key_findings': 'findings',
                'novelty_assessment': 'novelty'
            }
        } for i in range(10)
    ]

    topic = "AI Performance"

    # Mock query_groq to take some time
    def mock_query_groq(prompt, **kwargs):
        time.sleep(0.5)
        return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

    print("Benchmarking Stage 4 (Sequential)...")
    start_time = time.time()
    with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
        results = stage4_academic_scoring(analyzed_documents, topic)
    duration = time.time() - start_time
    print(f"Total time for 10 documents: {duration:.2f}s")
    assert len(results) == 10

if __name__ == "__main__":
    benchmark_stage4()
