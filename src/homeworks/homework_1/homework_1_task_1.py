from collections import Counter, OrderedDict, defaultdict
from typing import Callable, Dict, Generic, Optional, Type, TypeVar

ParentClass = TypeVar("ParentClass")

USER_TEXT = (
    "Registry with ParentClass 'dict', default=dict and Elements:\n"
    "\t1)Counter\n"
    "\t2)OrderedDict\n"
    "\t3)defaultdict\n"
    "Enter class name: "
)


class Registry(Generic[ParentClass]):
    def __init__(self, default: Optional[type] = None) -> None:
        self.default = default
        self.classes: Dict[str, Type[ParentClass]] = dict()

    def register(self, name: str) -> Callable[[Type[ParentClass]], Type[ParentClass]]:
        """Decorator for adding a class with a name into the register"""

        def inner(registered_class: Type[ParentClass]) -> Type[ParentClass]:
            self.classes[name] = registered_class
            return registered_class

        if name in self.classes:
            raise ValueError(f"{name} already in registry")
        return inner

    def dispatch(self, name: str) -> Type[ParentClass] | type:
        """Get class with a name from the register"""
        if name in self.classes:
            return self.classes[name]
        elif self.default is None:
            raise ValueError(f"{name} was not registered")
        else:
            return self.default


def main() -> None:
    register = Registry[dict](default=dict)
    register.register("Counter")(Counter)
    register.register("OrderedDict")(OrderedDict)
    register.register("defaultdict")(defaultdict)
    user_input = input(USER_TEXT)
    user_class = register.dispatch(user_input)
    print("Return:", user_class)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
