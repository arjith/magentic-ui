import pytest
from typing import Dict

from magentic_ui.tools.url_status_manager import (
    URL_ALLOWED,
    UrlStatusManager,
    UrlStatus,
)


@pytest.mark.asyncio
async def test_url_status_manager():
    """Test the URL status manager functionality."""

    url_statuses: Dict[str, UrlStatus] = {
        "example.com": URL_ALLOWED,
        "google.com": URL_ALLOWED,
        "http://www.bing.com": URL_ALLOWED,
        "ftp://filexfer.com": URL_ALLOWED,
        "sample.com/foo/bar": URL_ALLOWED,
        # Non-standard URL formats
        "localhost": URL_ALLOWED,
        "chrome-error://chromewebdata/": URL_ALLOWED,
    }

    url_status_manager = UrlStatusManager(url_statuses=url_statuses)

    assert url_status_manager.is_url_allowed("https://www.google.com")
    assert url_status_manager.is_url_allowed("http://google.com")
    assert url_status_manager.is_url_allowed("google.com/abcd")
    assert url_status_manager.is_url_allowed("https://www.bing.com")
    assert url_status_manager.is_url_allowed("ftp://www.filexfer.com/page")
    assert url_status_manager.is_url_allowed("subdomain.example.com")
    assert url_status_manager.is_url_allowed("sample.com/foo/bar/page.html")
    assert url_status_manager.is_url_allowed("http://localhost:8000")
    assert url_status_manager.is_url_allowed("https://localhost/file")
    assert url_status_manager.is_url_allowed("chrome-error://chromewebdata")
    assert url_status_manager.is_url_allowed("chrome-error://chromewebdata/page")

    assert not url_status_manager.is_url_allowed("example.org")
    assert not url_status_manager.is_url_allowed("ftp://google.com")
    assert not url_status_manager.is_url_allowed("bing.com")
    assert not url_status_manager.is_url_allowed("file://bing.com")
    assert not url_status_manager.is_url_allowed("notreallygoogle.com")
    assert not url_status_manager.is_url_allowed("http://filexfer.com")
    assert not url_status_manager.is_url_allowed("sample.com")
    assert not url_status_manager.is_url_allowed("sample.com/foo")
    assert not url_status_manager.is_url_allowed("sample.com/bar")


@pytest.mark.asyncio
async def test_explicit_block_list():
    url_status_manager = UrlStatusManager(
        url_statuses=None,
        explicit_block_list=["blocked.com/private"],
    )

    assert url_status_manager.is_url_blocked("blocked.com/private/page")
    assert not url_status_manager.is_url_allowed("blocked.com/private/page")


@pytest.mark.asyncio
async def test_url_match_with_query_and_fragment():
    url_statuses = {
        "example.com/path;param=value?foo=bar#frag": URL_ALLOWED,
    }
    url_status_manager = UrlStatusManager(url_statuses=url_statuses)

    assert url_status_manager.is_url_allowed(
        "https://example.com/path;param=value?foo=bar#frag"
    )
    assert not url_status_manager.is_url_allowed(
        "https://example.com/path;param=value?foo=bar#other"
    )
    assert not url_status_manager.is_url_allowed(
        "https://example.com/path;param=other?foo=bar#frag"
    )


@pytest.mark.asyncio
async def test_url_block_list_alias():
    manager = UrlStatusManager(url_statuses=None, url_block_list=["alias.com"])
    assert manager.is_url_blocked("alias.com/page")
