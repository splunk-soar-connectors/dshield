from soar_sdk.asset import AssetField, BaseAsset, FieldCategory


class Asset(BaseAsset):
    ip: str | None = AssetField(
        description="IP to Lookup for Test Connectivity",
        default="8.8.8.8",
        category=FieldCategory.CONNECTIVITY,
    )
