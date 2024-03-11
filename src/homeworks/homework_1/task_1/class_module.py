class Registry:
    def __init__(self, default=ValueError, base_class=None):
        self.default = default
        self.classes = dict()
        self.base_class = base_class

    def __getitem__(self, item: type):
        return Registry(self.default, item)

    def register(self, name: str):
        """Decorator for adding a class with a name into the register, if it is a subclass of the base_class"""

        def inner(registered_class: type):
            if issubclass(registered_class, self.base_class):
                self.classes[name] = registered_class

            return registered_class

        return inner

    def dispatch(self, name: str):
        """Get class with a name from the register"""
        if name in self.classes:
            return self.classes[name]
        elif self.default is ValueError:
            raise ValueError(f"{name} was not registered")
        else:
            return self.default
