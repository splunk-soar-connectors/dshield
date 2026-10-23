import ipaddress

from soar_sdk.abstract import SOARClient
from soar_sdk.action_results import ActionOutput, OutputField, PermissiveActionOutput
from soar_sdk.exceptions import ActionFailure
from soar_sdk.logging import getLogger
from soar_sdk.params import Param, Params

from ..app import app, Asset
from ..helper import lookup_ip as fetch_ip

logger = getLogger()


class LookupIpParams(Params):
    ip: str = Param(
        description="IP to Lookup",
        primary=True,
        cef_types=["ip", "ipv6"],
        column_name="IP",
    )


class AlexaOutput(ActionOutput):
    domains: int | None = OutputField(cef_types=["domain"])
    firstseen: str | None = None
    hostname: str | None = OutputField(cef_types=["host name"])
    lastrank: int | None = None
    lastseen: str | None = None


class FeedOutput(ActionOutput):
    firstseen: str | None = None
    lastseen: str | None = None


class ThreatfeedsOutput(PermissiveActionOutput):
    forumspam: FeedOutput | None = None
    matsnu: FeedOutput | None = None
    miner: FeedOutput | None = None


class LookupIpOutput(ActionOutput):
    alexa: AlexaOutput | None = None
    as_: int | None = OutputField(alias="as")
    asabusecontact: str | None = OutputField(cef_types=["email"])
    ascountry: str | None = None
    asname: str | None = None
    assize: int | None = None
    attacks: int | None = None
    cloud: str | None = None
    comment: str | None = None
    count: int | None = None
    maxdate: str | None = None
    maxrisk: str | None = None
    mindate: str | None = None
    network: str | None = None
    number: str | None = OutputField(cef_types=["ip", "ipv6"])
    threatfeeds: ThreatfeedsOutput | None = None
    updated: str | None = None


class LookupIpSummary(ActionOutput):
    count: int | None = OutputField(column_name="Count", example_values=[132])
    attacks: int | None = OutputField(column_name="Attacks", example_values=[23])
    mindate: str | None = OutputField(
        column_name="Min Date", example_values=["2020-12-19"]
    )
    maxdate: str | None = OutputField(
        column_name="Max Date", example_values=["2020-12-19"]
    )


@app.action(
    description="Get IP info from DShield",
    action_type="investigate",
    read_only=True,
    render_as="table",
    name="lookup ip",
    verbose='The <a href="https://isc.sans.edu/api/#ip">DShield API documentation page</a> explains the <i>count</i> and <i>attacks</i> values (found in the result) as:<ul><li><b>Count:</b> (also reports or records) total number of packets blocked from this IP</li><li><b>Attacks:</b> (also targets) number of unique destination IP addresses for these packets</li></ul>',
    summary_type=LookupIpSummary,
)
def lookup_ip(
    params: LookupIpParams, soar: SOARClient[LookupIpSummary], asset: Asset
) -> LookupIpOutput:
    logger.progress("Running action - handle lookup id")
    try:
        ipaddress.ip_address(params.ip)
    except ValueError as exc:
        raise ActionFailure("Please specify a valid IP to lookup") from exc

    response = fetch_ip(params.ip)
    data = response.get("ip")
    if not isinstance(data, dict):
        raise ActionFailure("Response not in the expected format")

    summary = LookupIpSummary(
        attacks=data.get("attacks"),
        count=data.get("count"),
        maxdate=data.get("maxdate"),
        mindate=data.get("mindate"),
    )
    soar.set_summary(summary)
    soar.set_message(
        f"Attacks: {summary.attacks}, Count: {summary.count}, "
        f"Maxdate: {summary.maxdate}, Mindate: {summary.mindate}"
    )
    return LookupIpOutput(**data)
