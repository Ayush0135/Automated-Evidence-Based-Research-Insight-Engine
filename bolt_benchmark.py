
import time
import json
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock the utils before importing stages
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

class TestBoltPerformance(unittest.TestCase):

    def setUp(self):
        # Reset mocks
        mock_llm.query_stage.reset_mock()
        mock_llm.query_gemini.reset_mock()
        mock_llm.query_groq.reset_mock()
        mock_search.google_search.reset_mock()
        mock_search.download_and_parse.reset_mock()

    def test_stage4_parallelism_and_order(self):
        print("\n--- Benchmarking Stage 4 Parallelism & Order ---")
        topic = "Quantum Computing"
        docs = [
            {"title": f"Doc {i}", "url": f"url{i}", "analysis": {"research_problem": "p", "methodology": "m", "key_findings": "f", "novelty_assessment": "n"}}
            for i in range(6)
        ]

        def slow_query_groq(prompt, **kwargs):
            time.sleep(0.5)
            return json.dumps({"score": 8, "strengths": "s", "weaknesses": "w"})

        mock_llm.query_groq.side_effect = slow_query_groq

        start_time = time.time()
        results = stage4_academic_scoring(docs, topic)
        end_time = time.time()

        elapsed = end_time - start_time
        print(f"Stage 4 elapsed time for 6 docs (3 workers, 0.5s delay): {elapsed:.2f}s")

        # Expected: ~1.0s (6 docs / 3 workers * 0.5s)
        self.assertLess(elapsed, 1.5, "Stage 4 is not parallelized correctly (too slow)")
        self.assertGreater(elapsed, 0.9, "Stage 4 is suspiciously fast")

        # Verify Order
        for i, res in enumerate(results):
            self.assertEqual(res['title'], f"Doc {i}", f"Order mismatched at index {i}")
        print("✅ Stage 4 order preservation verified.")

    def test_stage3_order(self):
        print("\n--- Benchmarking Stage 3 Order ---")
        docs = [
            {"title": f"Doc {i}", "raw_text": "Short text"}
            for i in range(4)
        ]

        def slow_query_gemini(prompt, **kwargs):
            # Extract doc title from prompt to simulate different responses
            if "Doc 0" in prompt: return json.dumps({"research_problem": "p0", "methodology": "m", "key_findings": "f", "novelty_assessment": "n", "research_gaps": "g", "novelty_assessment": "a", "technical_depth_score": 8, "missing_entities": "e"})
            if "Doc 1" in prompt: return json.dumps({"research_problem": "p1", "methodology": "m", "key_findings": "f", "novelty_assessment": "n", "research_gaps": "g", "novelty_assessment": "a", "technical_depth_score": 8, "missing_entities": "e"})
            if "Doc 2" in prompt: return json.dumps({"research_problem": "p2", "methodology": "m", "key_findings": "f", "novelty_assessment": "n", "research_gaps": "g", "novelty_assessment": "a", "technical_depth_score": 8, "missing_entities": "e"})
            if "Doc 3" in prompt: return json.dumps({"research_problem": "p3", "methodology": "m", "key_findings": "f", "novelty_assessment": "n", "research_gaps": "g", "novelty_assessment": "a", "technical_depth_score": 8, "missing_entities": "e"})
            return "{}"

        mock_llm.query_gemini.side_effect = slow_query_gemini

        results = stage3_document_analysis(docs)

        for i, res in enumerate(results):
            self.assertEqual(res['title'], f"Doc {i}", f"Stage 3 document order mismatched at index {i}")
        print("✅ Stage 3 document order preservation verified.")

    def test_stage3_chunk_order(self):
        print("\n--- Benchmarking Stage 3 Chunk Order ---")
        # Large doc to trigger chunking
        # 12000 chars per chunk. 26000 chars -> 3 chunks (0-12000, 11500-23500, 23000-26000)
        large_text = "A" * 26000
        docs = [{"title": "Large Doc", "raw_text": large_text}]

        def chunk_mock(prompt, **kwargs):
            if "Part 1" in prompt: return "Summary 1"
            if "Part 2" in prompt: return "Summary 2"
            if "Part 3" in prompt: return "Summary 3"
            # Final analysis prompt
            if "Content/Context:" in prompt:
                # Check if summaries are in order in the context
                if "Summary 1\nSummary 2\nSummary 3" in prompt:
                    return json.dumps({"research_problem": "ordered", "methodology": "m", "key_findings": "f", "novelty_assessment": "n", "research_gaps": "g", "novelty_assessment": "a", "technical_depth_score": 8, "missing_entities": "e"})
                else:
                    return json.dumps({"research_problem": "unordered", "methodology": "m", "key_findings": "f", "novelty_assessment": "n", "research_gaps": "g", "novelty_assessment": "a", "technical_depth_score": 8, "missing_entities": "e"})
            return "{}"

        mock_llm.query_gemini.side_effect = chunk_mock

        results = stage3_document_analysis(docs)
        self.assertEqual(results[0]['analysis']['research_problem'], "ordered", "Stage 3 chunk order scrambled!")
        print("✅ Stage 3 chunk order preservation verified.")

    def test_stage2_order(self):
        print("\n--- Benchmarking Stage 2 Order ---")
        decomposition = {
            'subtopics': [
                {
                    'name': 'Topic A',
                    'search_queries': ['query 1']
                }
            ]
        }

        mock_search.google_search.return_value = [
            {'link': f'url{i}', 'title': f'Title {i}', 'snippet': 'Topic A is great'} for i in range(5)
        ]

        def slow_download(url):
            # simulate different download times
            if "url0" in url: time.sleep(0.3)
            return "Some long enough text to pass the filter" * 20

        mock_search.download_and_parse.side_effect = slow_download

        results = stage2_document_discovery(decomposition)

        self.assertEqual(len(results), 5, "Stage 2 should have 5 results")
        for i, res in enumerate(results):
            self.assertEqual(res['url'], f'url{i}', f"Stage 2 download order mismatched at index {i}")
        print("✅ Stage 2 order preservation verified.")

if __name__ == '__main__':
    unittest.main()
