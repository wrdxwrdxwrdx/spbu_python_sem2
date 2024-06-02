import pytest

from src.homeworks.homework_3.ORM import *


@dataclass
class Info(JsonORM):
    a: str
    b: float


class TestJsonORM:
    @pytest.mark.parametrize(
        "json_dict",
        (
            ({"a": "1", "b": 2.1}),
            ({"a": "0", "d": 2.2}),
            ({"a": "a", "b": 0.12}),
        ),
    )
    def test_with_json(self, json_dict):
        obj = Info.with_json(json_dict)
        assert json_dict == obj.__json__

    @pytest.mark.parametrize(
        "json_dict",
        (
            ({"a": "1", "b": 2.1}),
            ({"a": "0", "b": 2.2}),
            ({"a": "a", "b": 0.12}),
        ),
    )
    def test_get_from_json(self, json_dict):
        obj = Info.with_json(json_dict)
        assert get_from_json(obj, "a") == json_dict["a"]
        assert get_from_json(obj, "b") == json_dict["b"]

    @pytest.mark.parametrize(
        "json_dict",
        (
            ({"a": "1", "b": 2.1}),
            ({"a": "0", "b": 2.2}),
            ({"a": "a", "b": 0.12}),
        ),
    )
    def test_get_from_json(self, json_dict):
        obj = Info.with_json(json_dict)
        assert get_from_json(obj, "a") == json_dict["a"]
        assert get_from_json(obj, "b") == json_dict["b"]

    @pytest.mark.parametrize(
        "json_dict",
        (
            ({"a": "1", "b": 2.1}),
            ({"a": "0", "b": 2.2}),
            ({"a": "a", "b": 0.12}),
        ),
    )
    def test_get_from_json_exception(self, json_dict):
        with pytest.raises(ValueError):
            obj = Info(**json_dict)
            assert get_from_json(obj, "d")

    @pytest.mark.parametrize(
        "json_dict",
        (
            ({"a": "1"}),
            ({"a": "0"}),
            ({"a": "a"}),
        ),
    )
    def test_get_from_json_exception_2(self, json_dict):
        with pytest.raises(ValueError):
            obj = Info.with_json(json_dict)
            assert get_from_json(obj, "b")


class TestLazyField:
    @pytest.mark.parametrize(
        "json_dict",
        (
            ({"a": "1", "b": 2.1}),
            ({"a": "0", "b": 2.2}),
            ({"a": "a", "b": 0.12}),
        ),
    )
    def test_get(self, json_dict):
        obj = Info.with_json(json_dict)
        assert "a" not in obj.__dict__
        _ = obj.a
        assert "a" in obj.__dict__
        assert obj.a == json_dict["a"]

        assert "b" not in obj.__dict__
        _ = obj.b
        assert "b" in obj.__dict__
        assert obj.b == json_dict["b"]
