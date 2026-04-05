
import time
import sys
import unittest
from unittest.mock import MagicMock, patch

# Define the mock query function BEFORE anything else
def stage3_mock_query_gemini(prompt, **kwargs):
    import re
    # Final summarization
    if "Analyze the following research document content" in prompt:
        if "Content/Context:" in prompt:
            context_part = prompt.split("Content/Context:")[1].split("Task:")[0].strip()
            # use a simpler regex for extraction in test
            summaries = re.findall(r"Summary \d+", context_part)
            # Use double quotes for JSON
            import json
            return json.dumps({
                "summaries": summaries,
                "research_problem": "p",
                "methodology": "m",
                "key_findings": "f",
                "limitations": "l",
                "research_gaps": "g",
                "novelty_assessment": "n",
                "technical_depth_score": 8,
                "missing_entities": "none"
            })

    # Chunk analysis
    match = re.search(r'Part (\d+)', prompt)
    if match:
        return f"Summary {match.group(1)}"

    return "{}"

# Mock the utils.llm and utils.search
mock_llm = MagicMock()
mock_search = MagicMock()

sys.modules['utils.llm'] = mock_llm
sys.modules['utils.search'] = mock_search

# Configure mocks
def slow_query(*args, **kwargs):
    time.sleep(0.5)
    return '{"score": 8, "strengths": "good", "weaknesses": "none"}'

mock_llm.query_groq.side_effect = slow_query
mock_llm.query_gemini.side_effect = stage3_mock_query_gemini

# NOW import the stages
import stages.stage3_analysis
import stages.stage4_scoring

class TestPerformance(unittest.TestCase):

    def test_stage4_parallelism(self):
        docs = [
            {"title": f"Doc {i}", "analysis": {"research_problem": "test"}}
            for i in range(6)
        ]

        start_time = time.time()
        results = stages.stage4_scoring.stage4_academic_scoring(docs, "test topic")
        end_time = time.time()

        duration = end_time - start_time
        print(f"\nStage 4 duration for 6 docs: {duration:.2f}s")

        # Parallel (3 workers): ceil(6/3) * 0.5 = 1.0s (+ overhead)
        self.assertLess(duration, 1.5, "Stage 4 is not performing in parallel as expected")
        self.assertEqual(len(results), 6)

        # Verify order preservation
        for i, doc in enumerate(results):
            self.assertEqual(doc['title'], f"Doc {i}", f"Order mismatched at index {i}")

    def test_stage3_order(self):
        # 26000 chars should give 3 chunks
        large_text = "A" * 26000
        doc = {
            "title": "Large Doc",
            "raw_text": large_text
        }

        # 1. Re-verify Stage 3 preserves ranking if multiple docs passed
        docs = [
            {"title": "Doc A", "raw_text": "Short"},
            {"title": "Doc B", "raw_text": "Short"}
        ]

        results = stages.stage3_analysis.stage3_document_analysis(docs)
        self.assertEqual(results[0]['title'], "Doc A")
        self.assertEqual(results[1]['title'], "Doc B")

        # 2. Now test chunking order within a single large doc
        with patch('stages.stage3_analysis.query_gemini', side_effect=stage3_mock_query_gemini):
            results = stages.stage3_analysis.stage3_document_analysis([doc])
            analysis = results[0].get('analysis', {})

            found_summaries = analysis.get('summaries', [])
            print(f"Stage 3 Found Summaries Order: {found_summaries}")

            # Expecting 3 chunks for 26000 chars
            self.assertTrue(len(found_summaries) >= 2, f"Doc was not chunked as expected, got {len(found_summaries)} summaries.")

            # Ensure summaries are in order: Summary 1, Summary 2, Summary 3...
            expected_summaries = [f"Summary {i+1}" for i in range(len(found_summaries))]
            self.assertEqual(found_summaries, expected_summaries, "Chunk order in Stage 3 was scrambled!")

if __name__ == "__main__":
    unittest.main()
