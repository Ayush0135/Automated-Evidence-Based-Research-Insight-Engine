import time
import sys
from unittest.mock import MagicMock

# Mock the utilities before importing stages
mock_search = MagicMock()
mock_llm = MagicMock()
mock_llm_offline = MagicMock()

sys.modules['utils.search'] = mock_search
sys.modules['utils.llm'] = mock_llm
sys.modules['utils.llm_offline'] = mock_llm_offline

# Import stages after mocking dependencies
from stages.stage2_discovery import stage2_document_discovery
from stages.stage3_analysis import stage3_document_analysis
from stages.stage4_scoring import stage4_academic_scoring

def test_pipeline_order():
    print("Testing Stage 2 order preservation...")
    # Mock search result: ensure it returns items in a specific order
    # Note: titles must contain 'Relevant' to pass Stage 2's heuristic relevance check
    mock_search.google_search.return_value = [
        {'link': f'url_{i}', 'title': f'Title {i} Relevant', 'snippet': f'Snippet {i}'}
        for i in range(5)
    ]
    # Simulate download delay to potentially trigger as_completed scrambling if it were still present
    def mock_download(url):
        idx = int(url.split('_')[1])
        # Later items take less time; as_completed would return them first
        time.sleep(0.1 * (5 - idx))
        return "Dummy text content " * 100

    mock_search.download_and_parse.side_effect = mock_download

    decomposition = {'subtopics': [{'name': 'Relevant', 'search_queries': ['query']}]}
    docs = stage2_document_discovery(decomposition)

    titles = [d['title'] for d in docs]
    print(f"Stage 2 titles: {titles}")
    assert titles == [f'Title {i} Relevant' for i in range(5)], f"Stage 2 order scrambled! Got: {titles}"

    print("\nTesting Stage 3 order preservation...")
    # Mock LLM analysis delay
    def mock_query_gemini(prompt, **kwargs):
        # Extract title from prompt to determine delay
        for i in range(5):
            if f"Title {i}" in prompt:
                time.sleep(0.1 * (5 - i))
                return '{"research_problem": "test"}'
        return '{"research_problem": "test"}'

    mock_llm.query_gemini.side_effect = mock_query_gemini

    analyzed_docs = stage3_document_analysis(docs)
    titles = [d['title'] for d in analyzed_docs]
    print(f"Stage 3 titles: {titles}")
    assert titles == [f'Title {i} Relevant' for i in range(5)], f"Stage 3 order scrambled! Got: {titles}"

    print("\nTesting Stage 4 order preservation...")
    # Mock Groq scoring delay
    def mock_query_groq(prompt, **kwargs):
        for i in range(5):
            if f"Title {i}" in prompt:
                time.sleep(0.1 * (5 - i))
                return '{"score": 8}'
        return '{"score": 8}'

    mock_llm.query_groq.side_effect = mock_query_groq

    scored_docs = stage4_academic_scoring(analyzed_docs, "topic")
    titles = [d['title'] for d in scored_docs]
    print(f"Stage 4 titles: {titles}")
    assert titles == [f'Title {i} Relevant' for i in range(5)], f"Stage 4 order scrambled! Got: {titles}"

    print("\nVerification SUCCESS: All modified stages preserve document order even with variable delays.")

if __name__ == "__main__":
    try:
        test_pipeline_order()
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
        sys.exit(1)
