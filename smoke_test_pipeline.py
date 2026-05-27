
import sys
import time
from unittest.mock import MagicMock, patch

# Mock all dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()
sys.modules['xhtml2pdf'] = MagicMock()
sys.modules['markdown'] = MagicMock()

# Mock search
mock_search = MagicMock()
sys.modules['utils.search'] = mock_search

# Create a small dummy pipeline test
def smoke_test_pipeline():
    print("Running Smoke Test Pipeline (Mocked)...")

    # Mocking Stage functions
    with patch('stages.stage1_topic.stage1_topic_decomposition') as s1, \
         patch('stages.stage2_discovery.stage2_document_discovery') as s2, \
         patch('stages.stage3_analysis.stage3_document_analysis') as s3, \
         patch('stages.stage3b_deepen.stage3b_deepen_research') as s3b, \
         patch('stages.stage4_scoring.stage4_academic_scoring') as s4, \
         patch('stages.stage5_filtering.stage5_selection_filtering') as s5, \
         patch('stages.stage6_synthesis.stage6_research_synthesis') as s6, \
         patch('stages.stage7_generation.stage7_paper_generation') as s7, \
         patch('stages.stage8_review.stage8_review_paper') as s8:

        s1.return_value = {'subtopics': []}
        s2.return_value = [{'title': 'D1'}]
        s3.return_value = [{'title': 'D1', 'analysis': {}}]
        s3b.return_value = []
        s4.return_value = [{'title': 'D1', 'scoring': {'score': 8}}]
        s5.return_value = [{'title': 'D1', 'scoring': {'score': 8}}]
        s6.return_value = "Synthesis"
        s7.return_value = "Final Paper Content"
        s8.return_value = {'score': 9, 'critique': 'Great'}

        from main import main
        with patch('sys.argv', ['main.py', 'test topic']):
            with patch('builtins.open', MagicMock()):
                main()

    print("Smoke Test Pipeline [OK]")

if __name__ == '__main__':
    smoke_test_pipeline()
