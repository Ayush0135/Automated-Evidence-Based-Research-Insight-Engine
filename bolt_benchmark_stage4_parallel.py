
import time
import sys
import json
from unittest.mock import MagicMock, patch

# Mocking external dependencies before importing stages
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['markdown'] = MagicMock()
sys.modules['xhtml2pdf'] = MagicMock()

# Now import the stage to benchmark
from stages.stage4_scoring import stage4_academic_scoring

def benchmark_stage4_parallel():
    print("Benchmarking Stage 4 (Parallel vs Sequential simulation)...")

    num_docs = 6
    docs = []
    for i in range(num_docs):
        docs.append({
            'title': f"Paper {i}",
            'analysis': {
                'research_problem': f'problem {i}',
                'methodology': f'method {i}',
                'key_findings': f'findings {i}',
                'novelty_assessment': f'novelty {i}'
            }
        })

    topic = "Performance Optimization"

    # Mock query_groq to simulate delay and return specific title in response
    # to verify order preservation.
    with patch('stages.stage4_scoring.query_groq') as mock_query:
        def side_effect(prompt, **kwargs):
            # Extract title from prompt to simulate model response for that specific doc
            # Title is after "Document Title: "
            title_part = prompt.split("Document Title: ")[1].split("\n")[0]
            time.sleep(1) # Simulate 1s delay per LLM call
            return json.dumps({
                "score": 8,
                "strengths": f"good for {title_part}",
                "weaknesses": "none"
            })

        mock_query.side_effect = side_effect

        print(f"Running parallel scoring for {num_docs} docs with 3 workers...")
        start_time = time.time()
        results = stage4_academic_scoring(docs, topic)
        end_time = time.time()

        duration = end_time - start_time
        print(f"\nTotal duration: {duration:.2f}s")
        print(f"Number of results: {len(results)}")

        # Verify order
        ordered_correctly = True
        for i, res in enumerate(results):
            expected_title = f"Paper {i}"
            if res['title'] != expected_title:
                print(f"ORDER MISMATCH: Expected {expected_title}, got {res['title']}")
                ordered_correctly = False
            else:
                # Also verify the scoring data matches the title (proves it wasn't just lucky timing)
                if expected_title not in res['scoring']['strengths']:
                    print(f"DATA MISMATCH: Scoring data for {res['title']} contains {res['scoring']['strengths']}")
                    ordered_correctly = False

        if ordered_correctly:
            print("SUCCESS: Document order and data integrity preserved.")
        else:
            print("FAILURE: Document order or data integrity compromised.")
            sys.exit(1)

        # 6 docs / 3 workers * 1s per doc = ~2s expected
        if duration < 3.0:
            print(f"SUCCESS: Speedup verified. Expected ~2s, got {duration:.2f}s")
        else:
            print(f"FAILURE: Speedup not as expected. Got {duration:.2f}s")
            sys.exit(1)

if __name__ == "__main__":
    benchmark_stage4_parallel()
