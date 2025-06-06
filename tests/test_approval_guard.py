import pytest
from magentic_ui.approval_guard import ApprovalGuard, ApprovalConfig
from autogen_core.models import UserMessage


@pytest.mark.asyncio
async def test_requires_approval_empty_context() -> None:
    guard = ApprovalGuard(input_func=None, default_approval=False)
    result = await guard.requires_approval(
        baseline="maybe", llm_guess="maybe", action_context=[]
    )
    assert result is False


@pytest.mark.asyncio
async def test_requires_approval_policies() -> None:
    guard = ApprovalGuard(
        input_func=None,
        default_approval=False,
        config=ApprovalConfig(approval_policy="auto-permissive"),
    )
    ctx = [UserMessage(content="test", source="user")]
    result = await guard.requires_approval(
        baseline="maybe", llm_guess="never", action_context=ctx
    )
    assert result is False
    result = await guard.requires_approval(
        baseline="always", llm_guess="never", action_context=ctx
    )
    assert result is True
