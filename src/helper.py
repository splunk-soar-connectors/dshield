import json
from urllib.parse import quote

import httpx

from soar_sdk.exceptions import ActionFailure

from .consts import API_URL, DEFAULT_TIMEOUT


def request(
    url: str,
    *,
    params: dict | str | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    verify_ssl: bool = True,
) -> httpx.Response:
    """Send an unauthenticated request to the public DShield API."""
    request_headers = {"User-Agent": "Splunk SOAR DShield app"}
    if headers:
        request_headers.update(headers)

    try:
        with httpx.Client(
            timeout=timeout,
            verify=verify_ssl,
            follow_redirects=False,
            headers=request_headers,
        ) as client:
            return client.get(url, params=params)
    except httpx.RequestError as exc:
        raise ActionFailure(f"Error connecting to server: {exc}") from exc


def lookup_ip(ip: str) -> dict:
    url = f"{API_URL}ip/{quote(ip, safe='')}?json"
    try:
        response = request(url)
        data = response.json()
    except ValueError as exc:
        details = response.text.replace("{", "").replace("}", "")
        raise ActionFailure(details) from exc

    if data.get("errors"):
        detail = json.dumps(data).replace("{", "").replace("}", "")
        raise ActionFailure(
            f"API failed, Status code: {response.status_code}, Detail: {detail}"
        )
    if response.status_code != 200:
        detail = json.dumps(data).replace("{", "").replace("}", "")
        raise ActionFailure(
            f"API failed, Status code: {response.status_code}, Detail: {detail}"
        )
    return data
