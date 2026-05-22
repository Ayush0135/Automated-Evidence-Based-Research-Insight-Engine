
import sys
from unittest.mock import MagicMock, patch

# Mock requests before importing search
mock_session = MagicMock()
mock_requests = MagicMock()
mock_requests.Session.return_value = mock_session

with patch.dict('sys.modules', {'requests': mock_requests}):
    from utils.search import google_search, download_and_parse

def test_google_search():
    print("Testing google_search...")
    mock_response = MagicMock()
    mock_response.json.return_value = {'items': [{'title': 'Test Result', 'link': 'http://example.com'}]}
    mock_session.get.return_value = mock_response

    results = google_search("test query")

    assert len(results) == 1
    assert results[0]['title'] == 'Test Result'
    mock_session.get.assert_called_once()
    print("google_search test passed!")

def test_download_and_parse():
    print("Testing download_and_parse...")
    mock_response = MagicMock()
    mock_response.content = b"<html><body><h1>Hello World</h1></body></html>"
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_session.get.return_value = mock_response

    # Reset mock to clear previous calls
    mock_session.get.reset_mock()

    text = download_and_parse("http://example.com")

    assert "Hello World" in text
    mock_session.get.assert_called_once()
    print("download_and_parse test passed!")

if __name__ == "__main__":
    try:
        test_google_search()
        test_download_and_parse()
        print("\nAll smoke tests passed!")
    except AssertionError as e:
        print(f"\nSmoke test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred during smoke testing: {e}")
        sys.exit(1)
