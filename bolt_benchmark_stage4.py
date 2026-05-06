
import time
import sys
import os
from unittest.mock import MagicMock

# Mock dependencies that might not be installed or need API keys
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['ollama'] = MagicMock()

# Import utils first so we can mock the function before it's imported elsewhere
import utils.llm as llm

# Mock query_groq to simulate LLM delay
def mock_query_groq(prompt, **kwargs):
    time.sleep(0.5) # Simulate 0.5s LLM latency
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

llm.query_groq = mock_query_groq

# Now we can import the stage which will use our mocked llm.query_groq
import stages.stage4_scoring as stage4

def benchmark_stage4():
    # Mock documents
    docs = []
    for i in range(10):
        docs.append({
            'title': f"Doc {i}",
            'analysis': {
                'research_problem': 'problem',
                'methodology': 'method',
                'key_findings': 'findings',
                'novelty_assessment': 'novelty'
            }
        })

    print(f"Benchmarking Stage 4 with {len(docs)} documents...")
    start_time = time.time()
    results = stage4.stage4_academic_scoring(docs, "test topic")
    end_time = time.time()

    duration = end_time - start_time
    print(f"\nTotal time: {duration:.2f} seconds")
    print(f"Documents scored: {len(results)}")

    # Verify order
    for i, doc in enumerate(results):
        if doc['title'] != f"Doc {i}":
            print(f"ORDER MISMATCH: Expected Doc {i}, got {doc['title']}")
        else:
            # print(f"Order OK for Doc {i}")
            pass

if __name__ == "__main__":
    benchmark_stage4()
