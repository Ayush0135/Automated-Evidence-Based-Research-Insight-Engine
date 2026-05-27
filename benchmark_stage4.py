
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
def benchmark_stage4(mock_query):
    docs = [
        {'title': f'Doc {i}', 'analysis': {'research_problem': 'P', 'methodology': 'M', 'key_findings': 'F', 'novelty_assessment': 'N'}}
        for i in range(5)
    ]

    print(f"Benchmarking Stage 4 Parallel Scoring with {len(docs)} documents...")
    start = time.time()
    scored_docs = stage4.stage4_academic_scoring(docs, "test topic")
    duration = time.time() - start

    print(f"Total time: {duration:.2f}s")
    # With 5 docs and 3 workers, we expect 2 batches of 1s each (roughly 2s total)
    # Sequential would take 5s.

    if duration < 3.0:
        print("SUCCESS: Parallelization confirmed (Duration < 3s)")
    else:
        print(f"FAILURE: Execution took too long ({duration:.2f}s)")

if __name__ == '__main__':
    benchmark_stage4()
