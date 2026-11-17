import msgspec


class BaseStruct(msgspec.Struct):
    """"""


class CamelizeBaseStruct(BaseStruct, rename="camel"):
    """"""
