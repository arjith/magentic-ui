# Callback Wrapper

Magentic-UI components rely on `pydantic` models for configuration. These models are serialized to YAML and later reloaded when constructing agent teams. Python callables normally cannot be serialized directly. The new `CallbackWrapper` class stores a dotted import path to a function so it can be referenced inside component configs.

Use `CallbackWrapper.from_callable(func)` to create one. When called, the wrapper dynamically imports the function and executes it. This allows callbacks like the approval guard lookup to be included in serialized config files.
