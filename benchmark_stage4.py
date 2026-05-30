import time
import sys
import os
from unittest.mock import MagicMock, patch

# Mock dependencies that might not be installed or need API keys
sys.modules['termcolor'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()

def mock_query_groq(prompt, **kwargs):
    # Simulate network latency
    time.sleep(1)
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

def benchmark_stage4():
    from stages.stage4_scoring import stage4_academic_scoring

    docs = []
    for i in range(5):
        docs.append({
            "title": f"Doc {i}",
            "analysis": {
                "research_problem": "problem",
                "methodology": "method",
                "key_findings": "findings",
                "novelty_assessment": "novel"
            }
        })

    print(f"Benchmarking stage4 with {len(docs)} documents...")

    with patch('stages.stage4_scoring.query_groq', side_effect=mock_query_groq):
        start_time = time.time()
        results = stage4_academic_scoring(docs, "test topic")
        end_time = time.time()

    duration = end_time - start_time
    print(f"Completed in {duration:.2f} seconds")
    return duration

if __name__ == "__main__":
    benchmark_stage4()
