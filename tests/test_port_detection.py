from magentic_ui.tools.playwright.browser.headless_docker_playwright_browser import (
    HeadlessDockerPlaywrightBrowser,
)
from magentic_ui.tools.playwright.browser.vnc_docker_playwright_browser import (
    VncDockerPlaywrightBrowser,
)
from pathlib import Path


class FakeContainer:
    def __init__(self, ports):
        self.attrs = {"NetworkSettings": {"Ports": ports}}

    def reload(self):
        pass


def test_headless_port_detection():
    browser = HeadlessDockerPlaywrightBrowser(playwright_port=37367)
    browser._container = FakeContainer({"37367/tcp": [{"HostPort": "49001"}]})
    browser._container_playwright_port = 37367
    browser._update_ports_from_container()
    assert browser._playwright_port == 49001


def test_vnc_port_detection():
    browser = VncDockerPlaywrightBrowser(bind_dir=Path("."))
    browser._container = FakeContainer(
        {
            "37367/tcp": [{"HostPort": "49002"}],
            "6080/tcp": [{"HostPort": "49003"}],
        }
    )
    browser._container_playwright_port = 37367
    browser._container_novnc_port = 6080
    browser._update_ports_from_container()
    assert browser._playwright_port == 49002
    assert browser._novnc_port == 49003
