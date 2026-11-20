import msgspec


class BaseStruct(msgspec.Struct):
    """Base class for shared API schemas."""


class CamelizeBaseStruct(BaseStruct, rename="camel"):
    """Base class for API schemas with camelCase serialized field names."""
