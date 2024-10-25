import pytest

from src.homeworks.Registry.Registry import *


class TestRegistry:
    class DummyClass:
        pass

    registry = Registry[DummyClass](default=dict)
    registry_no_default = Registry[DummyClass]()
    registry_dict = Registry[dict]()

    for name, new_class in [("OrderedDict", OrderedDict), ("defaultdict", defaultdict), ("Counter", Counter)]:
        registry_dict.register(name)(new_class)

    @registry.register("SubclassDummy1")
    @registry_no_default.register("SubclassDummy1")
    class SubclassDummy1(DummyClass):
        pass

    @registry.register("SubclassDummy2")
    @registry_no_default.register("SubclassDummy2")
    class SubclassDummy2(DummyClass):
        pass

    @pytest.mark.parametrize(
        "name,storage",
        [
            ("SubclassDummy1", registry),
            ("SubclassDummy2", registry),
            ("OrderedDict", registry_dict),
            ("defaultdict", registry_dict),
            ("Counter", registry_dict),
        ],
    )
    def test_registry_store_name(self, name, storage):
        assert name in storage.classes

    @pytest.mark.parametrize("name,expected", [("SubclassDummy1", SubclassDummy1), ("SubclassDummy2", SubclassDummy2)])
    def test_registry_store_class(self, name, expected):
        assert self.registry.classes[name] == expected

    @pytest.mark.parametrize(
        "name,my_class,storage",
        [
            ("SubclassDummy1", SubclassDummy1, registry),
            ("SubclassDummy2", SubclassDummy2, registry),
            ("OrderedDict", OrderedDict, registry_dict),
            ("defaultdict", defaultdict, registry_dict),
            ("Counter", Counter, registry_dict),
        ],
    )
    def test_dispatch(self, name, my_class, storage):
        assert storage.dispatch(name) == my_class

    @pytest.mark.parametrize(
        "name,default",
        [
            ("NotInRegistry_1", dict),
            ("NotInRegistry_2", dict),
        ],
    )
    def test_default_dispatch(self, name, default):
        assert self.registry.dispatch(name) == default

    def test_dispatch_exception(self):
        with pytest.raises(ValueError):
            self.registry_no_default.dispatch("NotInRegistry")

    @pytest.mark.parametrize(
        "name,new_class", [("OrderedDict", defaultdict), ("defaultdict", Counter), ("Counter", defaultdict)]
    )
    def test_register_exception(self, name, new_class):
        with pytest.raises(ValueError):
            self.registry_dict.register(name)(new_class)
