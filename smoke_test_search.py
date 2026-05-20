import sys
from unittest.mock import MagicMock, patch

# Mock dependencies that might be missing or require keys
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['ollama'] = MagicMock()

import utils.search as search

def test_search_functional_integrity():
    print("Running functional integrity test for utils.search...")

    with patch('utils.search.session') as mock_session:
        # Mock google_search behavior
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': [{'title': 'Test Result', 'link': 'http://example.com'}]}
        mock_session.get.return_value = mock_response

        results = search.google_search("test query")
        assert len(results) == 1
        assert results[0]['title'] == 'Test Result'
        print("  - google_search: PASSED")

        # Mock download_and_parse behavior (HTML)
        mock_html_response = MagicMock()
        mock_html_response.content = b"<html><body><h1>Test Page</h1><p>Content</p></body></html>"
        mock_html_response.headers = {'Content-Type': 'text/html'}
        mock_session.get.return_value = mock_html_response

        content = search.download_and_parse("http://example.com")
        assert "Test Page" in content
        assert "Content" in content
        print("  - download_and_parse (HTML): PASSED")

if __name__ == "__main__":
    try:
        test_search_functional_integrity()
        print("All functional tests PASSED.")
    except Exception as e:
        print(f"Functional test FAILED: {e}")
        sys.exit(1)
