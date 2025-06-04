# Editing Guide

This guide highlights common tasks for modifying Magentic-UI.

## Setting Up a Development Environment

1. Install the project with development dependencies:
   ```bash
   pip install -e .[dev]
   ```
2. Install Playwright browsers (needed for some tests):
   ```bash
   playwright install
   ```

## Running Checks

Use `poe check` to run formatting, linting and the test suite:

```bash
poe check
```

Some tests require Playwright browsers and may take time to run. If dependencies are missing, install them as shown above.

## Updating Documentation

Markdown documentation lives in the `docs/` folder. Keep documents concise and make sure to reference images using relative paths.

