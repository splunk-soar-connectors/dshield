import json
from urllib.parse import unquote, urlsplit

from pydantic import field_validator
from soar_sdk.action_results import MakeRequestOutput
from soar_sdk.exceptions import ActionFailure
from soar_sdk.params import MakeRequestParams as SDKMakeRequestParams, Param

from ..app import app
from ..consts import API_URL, DEFAULT_TIMEOUT
from ..helper import request


class MakeRequestParams(SDKMakeRequestParams):
    """Parameters for a GET request to a relative DShield API endpoint."""

    http_method: str = Param(
        description="HTTP method to use. DShield API requests use GET.",
        required=False,
        default="GET",
        value_list=["GET"],
    )
    endpoint: str = Param(
        description=(
            "Relative path under the DShield API, such as 'ipdetails/8.8.8.8' "
            "or 'intelfeed'. Do not include the API base URL or query string."
        ),
        required=True,
    )
    query_parameters: str | None = Param(
        description=(
            "Optional query parameters as a JSON object or query string. "
            "Use 'json' to request JSON output when supported by the endpoint."
        ),
        required=False,
    )
    body: str | None = Param(
        description="Not used. This action only supports GET requests.",
        required=False,
    )

    @field_validator("http_method")
    @classmethod
    def validate_http_method(cls, value: str) -> str:
        method = value.strip().upper()
        if method != "GET":
            raise ValueError("Only GET requests are supported")
        return method

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        endpoint = value.strip()
        if not endpoint or endpoint.startswith("//") or "\\" in endpoint:
            raise ValueError("Endpoint must be a relative path under the DShield API")

        decoded = endpoint
        for _ in range(len(endpoint)):
            next_value = unquote(decoded)
            if next_value == decoded:
                break
            decoded = next_value

        parsed = urlsplit(decoded)
        path = decoded.lstrip("/")
        if (
            not path
            or parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or "?" in endpoint
            or "#" in endpoint
            or decoded.startswith("//")
            or "\\" in decoded
            or any(part in {".", ".."} for part in path.split("/"))
            or any(ord(char) < 32 or ord(char) == 127 for char in decoded)
        ):
            raise ValueError("Endpoint must be a relative path under the DShield API")

        return endpoint.lstrip("/")


def _get_query_params(query_parameters: str | None) -> dict | str | None:
    if not query_parameters:
        return None
    try:
        parsed = json.loads(query_parameters)
    except (json.JSONDecodeError, TypeError):
        return query_parameters.lstrip("?") or None
    if not isinstance(parsed, dict):
        raise ActionFailure("Query parameters must be a JSON object or query string")
    return parsed or None


def _get_headers(headers_json: str | None) -> dict[str, str]:
    if not headers_json:
        return {}
    try:
        headers = json.loads(headers_json)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ActionFailure("Headers must be a JSON object") from exc
    if not isinstance(headers, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in headers.items()
    ):
        raise ActionFailure("Headers must be a JSON object with string keys and values")
    return headers


@app.make_request()
def make_request(params: MakeRequestParams) -> MakeRequestOutput:
    """Make an unauthenticated GET request to a DShield API endpoint."""
    endpoint = params.endpoint
    query_params = _get_query_params(params.query_parameters)
    headers = _get_headers(params.headers)
    if params.body:
        raise ActionFailure("GET requests cannot include a body")
    timeout = params.timeout if params.timeout is not None else DEFAULT_TIMEOUT
    url = f"{API_URL}{endpoint}"

    response = request(
        url,
        params=query_params,
        headers=headers,
        timeout=timeout,
        verify_ssl=params.verify_ssl,
    )
    return MakeRequestOutput(
        status_code=response.status_code,
        response_body=response.text,
    )


make_request.meta.read_only = True
