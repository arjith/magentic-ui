# Agent Guidelines

This repository uses automated agents to assist with development tasks. Please follow these rules when contributing via an agent:

1. **Run checks** – Before opening a pull request, run `poe check` if dependencies are available. This runs formatting, linting and tests.
2. **Testing limitations** – If checks fail because required dependencies cannot be installed, note this in your PR description.
3. **Documentation** – Add or update markdown files in the `docs/` folder when making significant changes.
4. **Style** – Keep lines under 120 characters and prefer descriptive commit messages.
5. **Playwright Setup** – If Playwright tests fail because browsers are missing, run `playwright install` before re-running `poe check`.

