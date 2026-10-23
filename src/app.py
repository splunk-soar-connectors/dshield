from soar_sdk.app import App

from .asset import Asset
from .connectivity import test_connectivity

app = App(
    name="DShield",
    app_type="reputation",
    logo="logo_dshield.svg",
    logo_dark="logo_dshield_dark.svg",
    product_vendor="DShield",
    product_name="DShield",
    publisher="Splunk",
    appid="efc1ac17-c75c-4c24-8233-161e68e8e7f4",
    fips_compliant=True,
    asset_cls=Asset,
)

app.test_connectivity()(test_connectivity)

from .actions import lookup_ip  # noqa: F401

if __name__ == "__main__":
    app.cli()
