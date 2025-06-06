# Code Overview

This document describes the main components of Magentic-UI so contributors can navigate the codebase more easily.

## Python Package

The Python source code lives under `src/magentic_ui`.

- `agents/` – definitions for the different agents (e.g. **Orchestrator**, **WebSurfer**, **Coder**, **FileSurfer**, and **UserProxy**).
- `backend/` – FastAPI backend that powers the web interface.
 - `tools/` – helper utilities used by the agents. For example, browser automation utilities live in `tools/playwright`. The `UrlStatusManager` here maintains allowed/rejected URL patterns along with an explicit block list for quick denies.
- `eval/` – scripts and utilities for running benchmarks.
- `task_team.py` and related modules – entry points for constructing agent teams.

Import the library via `import magentic_ui` or run the CLI with `magentic ui`.

## Frontend

The frontend is a [Gatsby](https://www.gatsbyjs.com/) application located in the `frontend/` directory. Source files are under `frontend/src`. The `package.json` there describes JavaScript dependencies.

## Tests

Unit tests reside in the `tests/` directory and can be executed with `pytest`. Some tests rely on `playwright`, which may require downloading browser binaries. See the [Editing Guide](editing-guide.md) for tips on running tests locally.

