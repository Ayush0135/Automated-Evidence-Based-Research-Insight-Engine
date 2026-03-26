import sys
import time
import json
import unittest
from unittest.mock import MagicMock, patch

# Mock modules before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()

# Configure mocks
def mock_query_llm(prompt, **kwargs):
    time.sleep(0.5) # Simulate LLM latency
    # Return a mock JSON for scoring if prompt contains "score"
    if "score" in prompt.lower():
        return json.dumps({"score": 8, "strengths": "Good", "weaknesses": "None"})
    # Return order-detectable summaries for analysis chunks
    if "Part 1" in prompt: return "SUMMARY_PART_1"
    if "Part 2" in prompt: return "SUMMARY_PART_2"
    if "Part 3" in prompt: return "SUMMARY_PART_3"
    # Return a mock JSON for analysis
    if "JSON strictly" in prompt:
        return json.dumps({
            "research_problem": "P",
            "methodology": "M",
            "key_findings": "F",
            "limitations": "L",
            "research_gaps": "G",
            "novelty_assessment": "N",
            "technical_depth_score": 5,
            "missing_entities": "E"
        })
    return "General summary content"

mock_llm.query_gemini.side_effect = mock_query_llm
mock_llm.query_groq.side_effect = mock_query_llm

def mock_google_search(query, num_results=5):
    # Include query in title to pass relevance filter if needed
    return [
        {'link': f'http://example.com/{query}_{i}', 'title': f'Paper {i} for {query}', 'snippet': f'Snippet for {query}'}
        for i in range(num_results)
    ]

def mock_download_and_parse(url):
    return "This is a long research paper content " * 100 # ~3000 chars

mock_search.google_search.side_effect = mock_google_search
mock_search.download_and_parse.side_effect = mock_download_and_parse

sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

class TestBoltOptimizations(unittest.TestCase):
    def test_stage4_parallelism(self):
        docs = [{'title': f'Doc {i}', 'analysis': {'research_problem': 'P', 'methodology': 'M', 'key_findings': 'F', 'novelty_assessment': 'N'}} for i in range(6)]
        topic = "Quantum Computing"

        start_time = time.time()
        results = stage4_academic_scoring(docs, topic)
        end_time = time.time()

        duration = end_time - start_time
        print(f"\nStage 4 duration: {duration:.2f}s")
        self.assertEqual(len(results), 6)
        # With 3 workers and 0.5s delay, it should take ~1.0s (2 batches of 3)
        self.assertLess(duration, 1.5)

    def test_stage3_order(self):
        # Create a document that will be chunked (> 12000 chars)
        # 3 chunks of 12000 chars with 500 overlap covers ~34000 chars.
        # Let's make it ~26000 chars to get 3 chunks precisely.
        doc = {
            'title': 'Large Paper',
            'raw_text': "A" * 26000
        }

        # We'll use a local mock to capture the order of chunk summaries
        # by checking how they are joined in the final prompt.
        # Since we can't easily intercept the internal join,
        # let's mock query_gemini for the final analysis call and check its input.

        call_args = []
        def capture_prompt(prompt, **kwargs):
            call_args.append(prompt)
            return mock_query_llm(prompt, **kwargs)

        with patch('stages.stage3_analysis.query_gemini', side_effect=capture_prompt):
            stage3_document_analysis([doc])

        # The last prompt should contain the concatenated summaries
        final_prompt = call_args[-1]
        self.assertIn("SUMMARY_PART_1\nSUMMARY_PART_2\nSUMMARY_PART_3", final_prompt)
        print("\nStage 3 order verification: SUCCESS")

if __name__ == "__main__":
    unittest.main()
