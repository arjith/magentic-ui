# Development Tasks

This document outlines outstanding tasks derived from `BUGS.md` and TODO comments in the source code.

## 1. Fix Playwright Test Failures
Playwright-based tests currently fail when browsers are not installed.

### Steps
1. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```
2. Install the required browsers:
   ```bash
   playwright install
   ```
3. Ensure `pytest_asyncio` is available:
   ```bash
   pip install pytest-asyncio
   ```
4. Run the test suite:
   ```bash
   poe test
   ```
   All tests should pass.

## 2. Resolve Pyright Type Errors
Static analysis reports multiple type errors.

### Steps
1. Run type checking:
   ```bash
   poe pyright
   ```
2. Add missing type hints and fix reported issues.
3. Re-run `poe pyright` until no errors remain.
4. Run `poe check` to ensure formatting, linting and tests still pass.

## 3. Address TODO Comments
Several TODO markers indicate incomplete implementations.

Key files include:
- `src/magentic_ui/tools/playwright/browser/vnc_docker_playwright_browser.py`
- `src/magentic_ui/tools/url_status_manager.py`
- `src/magentic_ui/backend/teammanager/teammanager.py`
- `src/magentic_ui/agents/_coder.py`
- `src/magentic_ui/agents/web_surfer/_web_surfer.py`
- `src/magentic_ui/agents/file_surfer/_code_markdown_file_browser.py`
- `frontend/src/components/features/Plans/PlanList.tsx`

### Steps
1. Search for `TODO` comments in each file.
2. Implement the missing logic or refactor as described.
3. After changes, run:
   ```bash
   poe check
   ```
   to confirm formatting, linting, type checking and tests all succeed.
## 4. Clean Up Documentation
Minor issues in the documentation can cause confusion for contributors.

### Steps
1. Fix known typos, such as the "questions to GitHub" wording in `SUPPORT.md`.
2. Review other markdown files for additional spelling or grammar mistakes.
3. After edits run:
   ```bash
   poe check
   ```
   to verify formatting and tests still pass.

Keep this document up to date as tasks are completed or new issues are discovered.
