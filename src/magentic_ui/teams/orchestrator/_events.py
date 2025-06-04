from pydantic import BaseModel


class GroupChatPause(BaseModel):
    """Event to pause the group chat."""

    ...


class GroupChatResume(BaseModel):
    """Event to resume the group chat."""

    ...
