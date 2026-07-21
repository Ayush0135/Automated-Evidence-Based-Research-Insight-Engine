import unittest
from unittest.mock import patch, MagicMock
from stages.stage2_discovery import stage2_document_discovery

class TestDeepenDeduplication(unittest.TestCase):
    @patch('stages.stage2_discovery.google_search')
    @patch('stages.stage2_discovery.download_and_parse')
    def test_cross_stage_deduplication(self, mock_download, mock_search):
        # Setup mock search results
        mock_search.return_value = [
            {
                "title": "Existing Doc Title",
                "link": "http://example.com/existing",
                "snippet": "This is an existing document that we want to skip."
            },
            {
                "title": "brand new paper",
                "link": "http://example.com/new",
                "snippet": "This is a brand new paper on deep dive refinement."
            }
        ]

        # Mock download to return valid length text so it doesn't get skipped as too short
        mock_download.return_value = "Valid research text content " * 50

        # Existing analyzed documents that should trigger deduplication
        existing_docs = [
            {
                "title": "Existing Doc Title",
                "url": "http://example.com/existing",
                "analysis": {}
            }
        ]

        decomposition_data = {
            'subtopics': [
                {
                    'name': 'Deep Dive Refinement',
                    'search_queries': ['deep dive query']
                }
            ]
        }

        # Run discovery with existing docs
        retrieved_docs = stage2_document_discovery(decomposition_data, existing_docs=existing_docs)

        # The document with URL "http://example.com/existing" or title "Existing Doc Title" should be skipped.
        # Only the "brand new paper" should be downloaded and returned.
        self.assertEqual(len(retrieved_docs), 1)
        self.assertEqual(retrieved_docs[0]['url'], "http://example.com/new")
        self.assertEqual(retrieved_docs[0]['title'], "brand new paper")

        # Verify download was called only for the new url
        mock_download.assert_called_once_with("http://example.com/new")

if __name__ == '__main__':
    unittest.main()
