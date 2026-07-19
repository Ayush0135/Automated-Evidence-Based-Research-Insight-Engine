import unittest
from unittest.mock import patch
from stages.stage2_discovery import stage2_document_discovery

class TestDeepenDeduplication(unittest.TestCase):
    @patch('stages.stage2_discovery.google_search')
    @patch('stages.stage2_discovery.download_and_parse')
    def test_deduplication_with_existing_sources(self, mock_download, mock_search):
        # Setup mock responses
        mock_search.return_value = [
            {
                "title": "Existing Title 1",
                "link": "https://example.com/existing-1",
                "snippet": "Existing snippet"
            },
            {
                "title": "Existing Title 2",
                "link": "https://example.com/existing-2",
                "snippet": "Another existing snippet"
            },
            {
                "title": "New Title",
                "link": "https://example.com/new-url",
                "snippet": "New and unique snippet about physics"
            }
        ]

        mock_download.return_value = "This is some dummy research paper content that is long enough to satisfy the 500 characters minimum requirement. " * 5

        # Create dummy decomposition data
        decomposition_data = {
            "subtopics": [
                {
                    "name": "physics",
                    "search_queries": ["physics search query"]
                }
            ]
        }

        # Define existing documents to filter out
        existing_urls = ["https://example.com/existing-1"]
        existing_titles = ["existing title 2"]  # lowercased and stripped

        # Call document discovery
        documents = stage2_document_discovery(
            decomposition_data,
            existing_urls=existing_urls,
            existing_titles=existing_titles
        )

        # It should filter out Existing Title 1 (due to URL) and Existing Title 2 (due to title matching)
        # So only "New Title" should be downloaded
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]["title"], "New Title")
        self.assertEqual(documents[0]["url"], "https://example.com/new-url")

        # Verify download_and_parse was only called once (for the new url)
        mock_download.assert_called_once_with("https://example.com/new-url")

if __name__ == "__main__":
    unittest.main()
