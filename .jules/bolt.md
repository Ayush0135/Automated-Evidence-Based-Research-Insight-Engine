## 2025-05-14 - Mocking Dependencies for LLM Utils
**Learning:** When creating benchmark or test scripts for modules that import `utils/llm.py`, it is necessary to mock `dotenv` (via `sys.modules['dotenv'] = MagicMock()`) in addition to the LLM provider libraries. Failing to do so causes `ModuleNotFoundError` because `utils/llm.py` calls `load_dotenv()` at the top level.
**Action:** Always include `dotenv` in the list of mocked modules when setting up a mock environment for project stages or utilities.
