from __future__ import annotations

import asyncio
import logging

from pathlib import Path
import secrets

from autogen_core import Component
import docker
from docker.models.containers import Container
from pydantic import BaseModel

from .base_playwright_browser import DockerPlaywrightBrowser


# Configure logging
logger = logging.getLogger(__name__)


class VncDockerPlaywrightBrowserConfig(BaseModel):
    """
    Configuration for the VNC Docker Playwright Browser.
    """

    bind_dir: Path
    image: str = "magentic-ui-vnc-browser"
    playwright_port: int = 37367
    novnc_port: int = 6080
    playwright_websocket_path: str | None = None
    inside_docker: bool = True


class VncDockerPlaywrightBrowser(
    DockerPlaywrightBrowser, Component[VncDockerPlaywrightBrowserConfig]
):
    """
    A Docker-based Playwright browser implementation with VNC support for visual interaction.
    Provides both programmatic browser control via Playwright and visual access through noVNC.

    Args:
        bind_dir (Path): Directory to bind mount into the container for file access.
        image (str, optional): Docker image name for the VNC-enabled browser. Default: "magentic-ui-vnc-browser".
        playwright_port (int, optional): Port for Playwright WebSocket connection. Default: 37367.
        playwright_websocket_path (str | None, optional): Custom WebSocket path. If None, generates random path.
        novnc_port (int, optional): Port for noVNC web interface. Default: 6080.
        inside_docker (bool, optional): Whether the client is running inside Docker. Default: True.
        network_name (str, optional): Docker network name for container communication. Default: `my-network`.

    Properties:
        browser_address (str): WebSocket URL for Playwright connection.
        vnc_address (str): HTTP URL for noVNC web interface.

    Example:
        ```python
        browser = VncDockerPlaywrightBrowser(
            bind_dir=Path("./workspace"),
            playwright_port=37367,
            novnc_port=6080
        )
        await browser.start()
        # Access browser programmatically via Playwright
        # Access visual interface via noVNC at browser.vnc_address
        await browser.close()
        ```

    Note:
        Requires the Docker image 'magentic-ui-vnc-browser' to be available locally.
        Build using the Dockerfile in docker/browser-docker directory.
    """

    component_config_schema = VncDockerPlaywrightBrowserConfig
    component_type = "other"

    def __init__(
        self,
        *,
        bind_dir: Path,
        image: str = "magentic-ui-vnc-browser",
        playwright_port: int = 37367,
        playwright_websocket_path: str | None = None,
        novnc_port: int = 6080,
        inside_docker: bool = True,
        network_name: str = "my-network",
    ):
        super().__init__()
        self._bind_dir = bind_dir
        self._image = image
        self._container_playwright_port = playwright_port
        self._container_novnc_port = novnc_port
        self._playwright_port = playwright_port
        self._novnc_port = novnc_port
        self._playwright_websocket_path = (
            playwright_websocket_path or secrets.token_hex(16)
        )
        self._inside_docker = inside_docker
        self._network_name = network_name
        self._hostname = (
            f"magentic-ui-vnc-browser_{self._playwright_websocket_path}_{self._novnc_port}"
            if inside_docker
            else "localhost"
        )
        self._docker_name = f"magentic-ui-vnc-browser_{self._playwright_websocket_path}_{self._novnc_port}"

    # TODO: This is a temporary solution to avoid port conflicts. Ideally we should allow docker to tell us which sockets to use
    def _generate_new_browser_address(self) -> None:
        """
        Generate new ports for Playwright and noVNC.
        """
        self._playwright_port = 0
        self._novnc_port = 0

    @property
    def browser_address(self) -> str:
        """
        Get the address of the Playwright browser.
        """
        return f"ws://{self._hostname}:{self._playwright_port}/{self._playwright_websocket_path}"

    @property
    def vnc_address(self) -> str:
        """
        Get the address of the noVNC server.
        """
        return f"http://{self._hostname}:{self._novnc_port}/vnc.html"

    @property
    def novnc_port(self) -> int:
        """
        Get the address of the noVNC server.
        """
        return self._novnc_port

    @property
    def playwright_port(self) -> int:
        """
        Get the address of the noVNC server.
        """
        return self._playwright_port

    async def create_container(self) -> Container:
        """
        Start a headless Playwright browser using the official Playwright Docker image.
        """
        logger.info(
            f"Starting headless Playwright browser on port {self._playwright_port}..."
        )

        client = docker.from_env()

        return await asyncio.to_thread(
            client.containers.create,
            name=self._docker_name,
            image=self._image,
            detach=True,
            auto_remove=True,
            network=self._network_name if self._inside_docker else None,
            ports={
                f"{self._container_playwright_port}/tcp": self._playwright_port,
                f"{self._container_novnc_port}/tcp": self._novnc_port,
            },
            volumes={
                str(self._bind_dir.resolve()): {"bind": "/workspace", "mode": "rw"}
            },
            environment={
                "PLAYWRIGHT_WS_PATH": self._playwright_websocket_path,
                "PLAYWRIGHT_PORT": str(self._container_playwright_port),
                "NO_VNC_PORT": str(self._container_novnc_port),
            },
        )

    def _update_ports_from_container(self) -> None:
        assert self._container is not None
        ports = self._container.attrs.get("NetworkSettings", {}).get("Ports", {})
        mapping = ports.get(f"{self._container_playwright_port}/tcp")
        if mapping:
            self._playwright_port = int(mapping[0]["HostPort"])
        mapping = ports.get(f"{self._container_novnc_port}/tcp")
        if mapping:
            self._novnc_port = int(mapping[0]["HostPort"])

    def _to_config(self) -> VncDockerPlaywrightBrowserConfig:
        return VncDockerPlaywrightBrowserConfig(
            bind_dir=self._bind_dir,
            image=self._image,
            playwright_port=self._playwright_port,
            novnc_port=self._novnc_port,
            playwright_websocket_path=self._playwright_websocket_path,
            inside_docker=self._inside_docker,
        )

    @classmethod
    def _from_config(
        cls, config: VncDockerPlaywrightBrowserConfig
    ) -> VncDockerPlaywrightBrowser:
        return cls(
            bind_dir=config.bind_dir,
            image=config.image,
            playwright_port=config.playwright_port,
            novnc_port=config.novnc_port,
            playwright_websocket_path=config.playwright_websocket_path,
            inside_docker=config.inside_docker,
        )
