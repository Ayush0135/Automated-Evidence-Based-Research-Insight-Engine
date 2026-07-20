import unittest
from unittest.mock import patch, MagicMock
from stages.stage2_discovery import stage2_document_discovery

class TestDeepenDeduplication(unittest.TestCase):
    @patch('stages.stage2_discovery.google_search')
    @patch('stages.stage2_discovery.download_and_parse')
    def test_stage2_discovery_deduplicates_by_url_and_title(self, mock_download, mock_search):
        # Setup mock for google search
        mock_search.return_value = [
            {
                "title": "Already Analyzed Paper",
                "link": "https://example.com/already-analyzed",
                "snippet": "A very nice deep dive paper about AI"
            },
            {
                "title": "Already Analyzed Title But Different URL",
                "link": "https://example.com/new-url",
                "snippet": "A very nice deep dive paper about AI"
            },
            {
                "title": "Brand New Paper",
                "link": "https://example.com/brand-new",
                "snippet": "A completely unique deep dive paper about AI"
            }
        ]

        # Setup mock for download_and_parse
        def download_side_effect(url):
            if url == "https://example.com/brand-new":
                return "This is a long content for the brand new paper that should easily pass the 500 characters minimum threshold. " * 10
            return ""
        mock_download.side_effect = download_side_effect

        decomposition_data = {
            'subtopics': [
                {
                    'name': 'Deep Dive Refinement',
                    'search_queries': ['AI deep learning models']
                }
            ]
        }

        existing_urls = {"https://example.com/already-analyzed"}
        existing_titles = {"already analyzed title but different url"}

        # Run discovery with existing URLs and titles
        results = stage2_document_discovery(
            decomposition_data,
            existing_urls=existing_urls,
            existing_titles=existing_titles
        )

        # We expect only "Brand New Paper" to be processed and downloaded
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Brand New Paper")
        self.assertEqual(results[0]['url'], "https://example.com/brand-new")

        # Verify download was only called for brand-new
        mock_download.assert_called_once_with("https://example.com/brand-new")

if __name__ == "__main__":
    unittest.main()
