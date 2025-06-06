import asyncio
import pytest
from pydantic import BaseModel
from autogen_core.models._model_client import ChatCompletionClient
from autogen_core.models._types import CreateResult, RequestUsage
from autogen_core import AgentId, CancellationToken
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import TextMessage

from magentic_ui.teams.orchestrator import GroupChat
from magentic_ui.teams.orchestrator._orchestrator import Orchestrator
from magentic_ui.teams.orchestrator.orchestrator_config import OrchestratorConfig


class DummyModelConfig(BaseModel):
    pass


class DummyChatCompletionClient(ChatCompletionClient):
    component_config_schema = DummyModelConfig
    component_provider_override = "tests.DummyChatCompletionClient"

    async def create(
        self,
        messages,
        *,
        tools=[],
        json_output=None,
        extra_create_args={},
        cancellation_token=None,
    ):
        return CreateResult(
            finish_reason="stop",
            content="",
            usage=RequestUsage(0, 0),
            cached=False,
        )

    async def create_stream(
        self,
        messages,
        *,
        tools=[],
        json_output=None,
        extra_create_args={},
        cancellation_token=None,
    ):
        if False:
            yield
        yield ""
        yield CreateResult(
            finish_reason="stop",
            content="",
            usage=RequestUsage(0, 0),
            cached=False,
        )

    def _to_config(self) -> DummyModelConfig:  # type: ignore[override]
        return DummyModelConfig()

    @classmethod
    def _from_config(cls, config: DummyModelConfig) -> "DummyChatCompletionClient":  # type: ignore[override]
        return cls()

    async def close(self) -> None:
        pass

    def actual_usage(self) -> RequestUsage:
        return RequestUsage(0, 0)

    def total_usage(self) -> RequestUsage:
        return RequestUsage(0, 0)

    def count_tokens(self, messages, *, tools=[]):
        return 0

    def remaining_tokens(self, messages, *, tools=[]):
        return 0

    @property
    def capabilities(self):
        return {}

    @property
    def model_info(self):
        return {}


class SimpleAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "simple agent")
        self.paused = False

    @property
    def produced_message_types(self):
        return (TextMessage,)

    async def on_messages(self, messages, cancellation_token: CancellationToken):
        return Response(chat_message=TextMessage(content="ok", source=self.name))

    async def on_pause(self, cancellation_token: CancellationToken) -> None:
        self.paused = True

    async def on_resume(self, cancellation_token: CancellationToken) -> None:
        self.paused = False

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        """Reset agent state; no-op for tests."""
        pass


@pytest.mark.asyncio
async def test_pause_resume_events():
    agent1 = SimpleAgent("assistant")
    user = SimpleAgent("user_proxy")
    model_client = DummyChatCompletionClient()
    gc = GroupChat(
        participants=[agent1, user],
        model_client=model_client,
        orchestrator_config=OrchestratorConfig(),
    )
    runtime = gc._runtime
    runtime.start()
    await gc._init(runtime)
    await gc.pause()
    await asyncio.sleep(0.05)
    orchestrator = await runtime.try_get_underlying_agent_instance(
        AgentId(type=gc._group_chat_manager_topic_type, key=gc._team_id),
        type=Orchestrator,
    )
    assert agent1.paused
    assert orchestrator._state.is_paused
    await gc.resume()
    await asyncio.sleep(0.05)
    assert not agent1.paused
    assert not orchestrator._state.is_paused
    runtime.stop()
