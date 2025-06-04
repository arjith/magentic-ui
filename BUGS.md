# Known Bugs and Tasks

This document lists issues found after running the repository's tests and linters.

## Failed Tests
Playwright based tests fail because the browsers are not installed. Example output:

```
sEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.                               [100%]
==================================== ERRORS ====================================
____ ERROR at setup of TestPlaywrightController.test_get_interactive_rects _____
...
>           browser = await pw.chromium.launch(headless=True)
```

The run ends with many errors:

```
ERROR tests/test_playwright_state.py::test_load_state_basic - playwright._impl...
ERROR tests/test_playwright_state.py::test_load_state_error_handling - playwr...
1 passed, 1 skipped, 2 warnings, 40 errors in 21.53s
```

Install the browsers with `playwright install` and ensure `pytest_asyncio` is installed.

## Pyright Type Errors
Static analysis via `pyright` reports numerous issues:

```
/workspace/magentic-ui/samples/sample_azure_agent.py:42:10 - error: Type of "project_client" is unknown
/workspace/magentic-ui/samples/sample_azure_agent.py:46:28 - error: Argument type is unknown
...
```

The log ends with:

```
/workspace/magentic-ui/tests/test_playwright_state.py:46:9 - error: Type of "append" is partially unknown
/workspace/magentic-ui/tests/test_playwright_state.py:49:11 - error: Type of "bring_to_front" is unknown
356 errors, 0 warnings, 0 informations
```

These require additional type hints or code adjustments.

## TODOs in Source Code
Several files contain TODO comments indicating incomplete implementations or design decisions:

- `src/magentic_ui/tools/playwright/browser/vnc_docker_playwright_browser.py` – temporary port selection.
- `src/magentic_ui/tools/url_status_manager.py` – refactor URL status logic and handle query/fragment parts.
- `src/magentic_ui/teams/orchestrator/_group_chat.py` – `pause` method needs event-based approach.
- `src/magentic_ui/approval_guard.py` – improve callback handling and approval logic.
- `src/magentic_ui/backend/teammanager/teammanager.py` – notes about run directory handling and config persistence.

Addressing these TODOs and fixing the failing tests will improve code quality.
