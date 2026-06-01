
import time
import sys
from unittest.mock import MagicMock, patch

# Mock the entire utils.llm module
mock_llm = MagicMock()
sys.modules['utils.llm'] = mock_llm

import stages.stage4_scoring

def benchmark():
    docs = [
        {
            'title': f'Doc {i}',
            'analysis': {
                'research_problem': 'problem',
                'methodology': 'method',
                'key_findings': 'findings',
                'novelty_assessment': 'novelty'
            }
        } for i in range(5)
    ]

    # Mock query_groq to take some time
    def slow_query(*args, **kwargs):
        time.sleep(1)
        return '{"score": 8, "strengths": "Good", "weaknesses": "None"}'

    # Use patch to ensure the stage4_scoring uses our mock
    with patch('stages.stage4_scoring.query_groq', side_effect=slow_query):
        start_time = time.time()
        results = stages.stage4_scoring.stage4_academic_scoring(docs, "test topic")
        end_time = time.time()

    print(f"Time taken for 5 documents: {end_time - start_time:.2f} seconds")
    return end_time - start_time

if __name__ == "__main__":
    benchmark()
