import json
import asyncio
from pathlib import Path
import types
import sys
import pytest

# Skip if core dependencies are missing
try:
    from magentic_ui.backend.teammanager import teammanager as tm_mod
    from magentic_ui.backend.teammanager.teammanager import TeamManager
    from magentic_ui.types import RunPaths
except Exception:
    pytest.skip("magentic_ui dependencies not installed", allow_module_level=True)


class DummyWebSurfer:
    def __init__(self, novnc_port, playwright_port):
        self.novnc_port = novnc_port
        self.playwright_port = playwright_port
        self.input_func = None


class DummyTeam:
    def __init__(self, surfer):
        self._participants = [surfer]

    async def close(self):
        pass


async def fake_get_task_team(*, magentic_ui_config=None, input_func=None, paths=None):
    surfer = DummyWebSurfer(
        magentic_ui_config.novnc_port, magentic_ui_config.playwright_port
    )
    return DummyTeam(surfer)


def fake_get_browser_resource_config(
    bind_dir, novnc_port=-1, playwright_port=-1, inside_docker=True
):
    if novnc_port == -1:
        novnc_port = 1111
    if playwright_port == -1:
        playwright_port = 2222
    return object(), novnc_port, playwright_port


@pytest.mark.asyncio
async def test_port_persistence(tmp_path, monkeypatch):
    monkeypatch.setattr(tm_mod, "get_task_team", fake_get_task_team)
    monkeypatch.setattr(tm_mod, "WebSurfer", DummyWebSurfer)
    monkeypatch.setattr(
        tm_mod, "get_browser_resource_config", fake_get_browser_resource_config
    )

    manager = TeamManager(tmp_path, tmp_path, inside_docker=False)
    paths = manager.prepare_run_paths()
    _, novnc1, play1 = await manager._create_team({}, paths=paths)
    meta_file = paths.external_run_dir / "run_metadata.json"
    with open(meta_file) as f:
        data = json.load(f)
    assert data["novnc_port"] == novnc1
    assert data["playwright_port"] == play1

    await manager.close()

    manager2 = TeamManager(tmp_path, tmp_path, inside_docker=False)
    paths2 = manager2.prepare_run_paths()
    _, novnc2, play2 = await manager2._create_team({}, paths=paths2)

    assert novnc2 == novnc1
    assert play2 == play1
    assert paths2.internal_run_dir == paths.internal_run_dir
    await manager2.close()
