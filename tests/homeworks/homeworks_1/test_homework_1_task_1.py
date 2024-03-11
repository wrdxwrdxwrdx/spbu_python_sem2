from src.homeworks.homework_1.task_1.class_module import *
import pytest


class DummyClass:
    pass


registry = Registry(default=dict)[DummyClass]
registry_no_default = Registry()[DummyClass]


@registry.register("SubclassDummy1")
@registry_no_default.register("SubclassDummy1")
class SubclassDummy1(DummyClass):
    pass


@registry.register("SubclassDummy2")
@registry_no_default.register("SubclassDummy2")
class SubclassDummy2(DummyClass):
    pass


@registry.register("NotSubclass")
@registry_no_default.register("NotSubclass")
class NotSubclass:
    pass


@pytest.mark.parametrize("name,expected", [("SubclassDummy1", True), ("SubclassDummy2", True), ("NotSubclass", False)])
def test_registry_store_name(name, expected):
    assert (name in registry.classes) == expected


@pytest.mark.parametrize("name,expected", [("SubclassDummy1", SubclassDummy1), ("SubclassDummy2", SubclassDummy2)])
def test_registry_store_class(name, expected):
    assert registry.classes[name] == expected


@pytest.mark.parametrize(
    "name,my_class,base_class",
    [
        ("SubclassDummy1", SubclassDummy1, DummyClass),
        ("SubclassDummy2", SubclassDummy2, DummyClass),
        ("NotSubclass", dict, dict),
    ],
)
def test_dispatch(name, my_class, base_class):
    assert registry.dispatch(name) == my_class and issubclass(registry.dispatch(name), base_class)


def test_dispatch_exception():
    with pytest.raises(ValueError):
        registry_no_default.dispatch("NotSubclass")
