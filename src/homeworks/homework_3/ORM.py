import json
from dataclasses import asdict, dataclass
from typing import Any, Type, TypeVar, get_args, get_origin

BASIC_TYPES = {int, float, str, list, tuple}


class LazyField:
    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def __get__(self, instance: "JsonORM", owner: "JsonORM") -> None:
        if self.field_name not in instance.__dict__:
            instance.__dict__[self.field_name] = get_from_json(instance, self.field_name)
        return instance.__dict__[self.field_name]

    def __set__(self, instance: "JsonORM", value: "JsonORM") -> None:
        pass


T = TypeVar("T")


@dataclass()
class JsonORM:
    @classmethod
    def with_json(cls: Type[T], json_dict: dict, strict: bool = False) -> T:
        if strict and json_dict.__annotations__ != cls.__annotations__:
            raise ValueError("json structure is different")
        for field_name in cls.__annotations__:
            setattr(cls, field_name, LazyField(field_name))
        obj = cls(*[None for _ in cls.__annotations__])
        setattr(obj, "__json__", json_dict)
        return obj

    def dump(self) -> str:
        return json.dumps(asdict(self))


def get_from_json(json_orm: JsonORM, field_name: str) -> Any:
    if not hasattr(json_orm, "__json__"):
        raise ValueError("No json in JsonORM")

    field_type = json_orm.__annotations__[field_name]
    json_dict = getattr(json_orm, "__json__")
    if field_name not in json_dict:
        raise ValueError(f"No {field_name} in json")
    field_value = json_dict[field_name]
    if field_type in BASIC_TYPES or get_origin(field_type) in BASIC_TYPES:
        origin = get_origin(field_type)
        if origin == list:
            list_element_type = get_args(field_type)[0]
            if list_element_type in BASIC_TYPES:
                return field_type(field_value)
            else:
                return [list_element_type.with_json(json) for json in field_value]
        return field_type(field_value)
    return field_type.with_json(json_dict[field_name])
