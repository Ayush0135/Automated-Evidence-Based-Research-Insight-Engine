# Bolt's Performance Journal

## 2025-05-14 - Pre-import Mocking for "from module import function"
**Learning:** When a module uses `from x import y`, mocking `x.y` after the module has been imported does not affect the already imported reference in the target module.
**Action:** Configure mock side effects or return values *before* importing the stage/module under test in benchmark scripts to ensure the target module receives the configured mock instance.
