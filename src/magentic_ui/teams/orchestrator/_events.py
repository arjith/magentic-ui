"""Events used by the orchestrator team implementation."""

# Re-export the base group chat events so that our orchestrator inherits the
# exact same types as :class:`autogen_agentchat.teams.BaseGroupChatManager`.
# This avoids typing mismatches when overriding methods that handle these
# events.

from autogen_agentchat.teams._group_chat._events import (
    GroupChatPause,
    GroupChatResume,
)

__all__ = ["GroupChatPause", "GroupChatResume"]
