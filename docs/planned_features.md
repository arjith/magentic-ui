# Planned Features

This document outlines proposed enhancements for Magentic-UI.
Each section breaks down the feature into tasks with implementation guidance, testing steps and fallback options.

## 1. Automatic Port Allocation for Docker Browsers
The Playwright browsers currently rely on pre-selected ports which can conflict
with running services.

### Tasks
1. Update `VncDockerPlaywrightBrowser._generate_new_browser_address` so Docker
   assigns free host ports. Inspect the container's `NetworkSettings` after
   creation and store the mapped host ports.
2. Refactor `HeadlessDockerPlaywrightBrowser` similarly.
3. Add unit tests in `tests/test_port_detection.py` to cover the new logic.
4. Ensure `task_team.py` propagates the dynamic ports when starting browser
   resources.

### Testing
- Run `poe check` after installing development dependencies.
- Manually start a team and verify that each browser uses unique ports.

### Contingencies
- If Docker APIs fail to report host ports, fall back to the current random port
  generation.
- Search Docker documentation for `Container.attrs["NetworkSettings"]["Ports"]`
  examples if mapping extraction fails.

## 2. Memory-Based Plan Suggestions
Leverage the existing `MemoryControllerProvider` to surface relevant plans when
creating new sessions.

### Tasks
1. Expose an endpoint under `backend` to retrieve plans via
   `MemoryController.retrieve_relevant_memos`.
2. Add a React component that queries this endpoint whenever a new task is typed
   on the landing page.
3. Allow the user to accept a suggestion which pre-populates the plan editor.
4. Record accepted plans back into memory for future runs.

### Testing
- Mock the backend endpoint with unit tests.
- Run the frontend in development mode and confirm plans appear as suggestions.

### Contingencies
- If memory retrieval errors occur, log them and fall back to a blank plan.
- Review Autogen documentation on `task_centric_memory` for configuration help.

## 3. Screenshot Timeline Viewer
Screenshots are already captured by the `WebSurfer` agent but they are not shown
in the UI.

### Tasks
1. Add an API route that lists screenshot files from the current run directory.
2. Create a new sidebar tab in the frontend to display screenshots in time
   order. Fetch images from the new route and allow stepping through them.
3. Update `WebSurfer` docs explaining how to enable `to_save_screenshots` and
   where screenshots are stored.

### Testing
- Enable screenshot saving in a local run and verify the viewer lists all files.
- Use Playwright tests (if browsers are available) to ensure the route returns
  the correct data.

### Contingencies
- If filesystem access fails, show an error message in the viewer and continue
  without screenshots.

