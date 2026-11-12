import ipaddress

from soar_sdk.abstract import SOARClient

from .asset import Asset
from .consts import CONNECTIVITY_FAILURE, CONNECTIVITY_SUCCESS
from .helper import lookup_ip


def test_connectivity(soar: SOARClient, asset: Asset) -> None:
    ip = asset.ip or "70.91.145.10"
    try:
        ipaddress.ip_address(ip)
        lookup_ip(ip)
    except Exception as exc:
        soar.set_message(f"{CONNECTIVITY_FAILURE}: {exc}")
        raise
    soar.set_message(CONNECTIVITY_SUCCESS)
