
import time
import json
import sys
from unittest.mock import MagicMock

# Mocking dependencies for the pipeline
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['bs4'] = MagicMock()
sys.modules['PyPDF2'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

# Now we can import the stage
import stages.stage4_scoring

# Setup mock LLM response with delay
def mock_query_groq(prompt, json_mode=False, fallback_to_others=True):
    time.sleep(0.5) # Simulated latency
    return json.dumps({
        "score": 8,
        "strengths": "Good methodology",
        "weaknesses": "Needs more data"
    })

# Patch the imported function in the stage module
stages.stage4_scoring.query_groq = mock_query_groq

def run_benchmark():
    topic = "AI in Healthcare"
    docs = []
    for i in range(10):
        docs.append({
            "title": f"Paper {i}",
            "analysis": {
                "research_problem": "Problem",
                "methodology": "Method",
                "key_findings": "Findings",
                "novelty_assessment": "Novelty"
            }
        })

    print(f"Starting benchmark for Stage 4 with {len(docs)} documents...")
    start_time = time.perf_counter()
    results = stages.stage4_scoring.stage4_academic_scoring(docs, topic)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Benchmark finished in {duration:.2f} seconds.")

    # Verify results
    assert len(results) == 10
    for i, doc in enumerate(results):
        assert doc['title'] == f"Paper {i}"
        assert 'scoring' in doc
        assert doc['scoring']['score'] == 8

    return duration

if __name__ == "__main__":
    run_benchmark()
