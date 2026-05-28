
import sys
from unittest.mock import MagicMock

# Mocking all dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()
sys.modules['utils.search'] = MagicMock()

# Mocking internal stages
sys.modules['stages.stage1_topic'] = MagicMock()
sys.modules['stages.stage2_discovery'] = MagicMock()
sys.modules['stages.stage3_analysis'] = MagicMock()
sys.modules['stages.stage3b_deepen'] = MagicMock()
# We don't mock stage4 to test our changes
sys.modules['stages.stage5_filtering'] = MagicMock()
sys.modules['stages.stage6_synthesis'] = MagicMock()
sys.modules['stages.stage7_generation'] = MagicMock()
sys.modules['stages.stage8_review'] = MagicMock()

# Mocking utils.llm
mock_llm = MagicMock()
mock_llm.query_groq = MagicMock(return_value='{"score": 7, "strengths": "ok", "weaknesses": "none"}')
sys.modules['utils.llm'] = mock_llm

import main
from stages.stage4_scoring import stage4_academic_scoring

def smoke_test():
    print("Running Smoke Test Pipeline...")

    # Minimal mock data to flow through the pipeline parts we care about
    docs = [{"title": "Smoke Doc", "analysis": {"research_problem": "P", "methodology": "M", "key_findings": "F", "novelty_assessment": "N"}}]

    # Test Stage 4 directly in its new parallel form
    scored = stage4_academic_scoring(docs, "Smoke Topic")

    if len(scored) == 1 and 'scoring' in scored[0]:
        print("Smoke Test Passed!")
    else:
        print("Smoke Test Failed!")
        sys.exit(1)

if __name__ == "__main__":
    smoke_test()
