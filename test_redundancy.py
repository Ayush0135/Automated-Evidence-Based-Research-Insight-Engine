import unittest
from unittest.mock import patch, MagicMock
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import chunk_text, analyze_single_document

class TestOptimizations(unittest.TestCase):
    def test_stage2_cross_stage_deduplication(self):
        # Sample decomposition data
        decomp_data = {
            'subtopics': [
                {
                    'name': 'Test Subtopic',
                    'search_queries': ['query 1']
                }
            ]
        }

        # We will mock google_search and download_and_parse
        with patch('stages.stage2_discovery.google_search') as mock_search, \
             patch('stages.stage2_discovery.download_and_parse') as mock_download:

            mock_search.return_value = [
                {'link': 'http://example.com/paper1.pdf', 'title': 'Paper 1 Title Subtopic', 'snippet': 'Snippet 1'},
                {'link': 'http://example.com/paper2.pdf', 'title': 'Paper 2 Title Subtopic', 'snippet': 'Snippet 2'},
                {'link': 'http://example.com/paper3.pdf', 'title': 'Paper 3 Title Subtopic', 'snippet': 'Snippet 3'},
            ]

            mock_download.return_value = "This is some dummy raw text that is long enough to be considered a research paper. " * 20

            # Case 1: No existing URLs or titles
            results = stage2_document_discovery(decomp_data)
            self.assertEqual(len(results), 3)

            # Case 2: One URL is already seen in previous stages
            existing_urls = {'http://example.com/paper1.pdf'}
            results_dup_url = stage2_document_discovery(decomp_data, existing_urls=existing_urls)
            # paper1 should be skipped, so only paper2 and paper3 are returned
            self.assertEqual(len(results_dup_url), 2)
            self.assertNotIn('http://example.com/paper1.pdf', [r['url'] for r in results_dup_url])

            # Case 3: One title (normalized) is already seen in previous stages
            existing_titles = {'paper 2 title subtopic'}
            results_dup_title = stage2_document_discovery(decomp_data, existing_titles=existing_titles)
            # paper2 should be skipped, so only paper1 and paper3 are returned
            self.assertEqual(len(results_dup_title), 2)
            self.assertNotIn('Paper 2 Title Subtopic', [r['title'] for r in results_dup_title])

    def test_stage3_chunking_threshold(self):
        # 120,000 characters (less than 128,000 threshold)
        text_short = "a" * 120000
        chunks_short = chunk_text(text_short)
        # Should result in 1 chunk
        self.assertEqual(len(chunks_short), 1)
        self.assertEqual(len(chunks_short[0]), 120000)

        # 250,000 characters (more than 128,000 threshold)
        text_long = "b" * 250000
        chunks_long = chunk_text(text_long)
        # 250,000 chars split into chunks of 128,000 with 2,000 overlap:
        # chunk 1: 0 - 128,000
        # chunk 2: start = 128,000 - 2,000 = 126,000. end = 126,000 + 128,000 = 250,000 (len 124,000)
        # So it should be exactly 2 chunks
        self.assertEqual(len(chunks_long), 2)
        self.assertEqual(len(chunks_long[0]), 128000)
        self.assertEqual(len(chunks_long[1]), 124000)

if __name__ == "__main__":
    unittest.main()
