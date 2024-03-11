from typing import Callable, Dict, Optional


class Registry:
    def __init__(self, default: Optional[type] = None) -> None:
        self.default = default
        self.classes: Dict[str, type] = dict()

    def __getitem__(self, item: type) -> "Registry":
        self.base_class = item
        return self

    def register(self, name: str) -> Callable[[type], type]:
        """Decorator for adding a class with a name into the register, if it is a subclass of the base_class"""

        def inner(registered_class: type) -> type:
            if issubclass(registered_class, self.base_class):
                self.classes[name] = registered_class

            return registered_class

        return inner

    def dispatch(self, name: str) -> type:
        """Get class with a name from the register"""
        if name in self.classes:
            return self.classes[name]
        elif self.default is None:
            raise ValueError(f"{name} was not registered")
        else:
            return self.default
