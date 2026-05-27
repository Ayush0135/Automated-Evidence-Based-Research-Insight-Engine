
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock the session to avoid real network calls
with patch('requests.Session') as mock_session_class:
    mock_session = mock_session_class.return_value
    from utils.search import google_search, download_and_parse

class TestSearchOptimization(unittest.TestCase):
    @patch('utils.search.session')
    def test_google_search_uses_session(self, mock_sess):
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': [{'title': 'Test Result'}]}
        mock_sess.get.return_value = mock_response

        results = google_search("test query")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Result')
        mock_sess.get.assert_called_once()

    @patch('utils.search.session')
    def test_download_and_parse_uses_session(self, mock_sess):
        mock_response = MagicMock()
        mock_response.content = b"<html><body>Test Content</body></html>"
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_sess.get.return_value = mock_response

        text = download_and_parse("http://example.com")

        self.assertIn("Test Content", text)
        mock_sess.get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
