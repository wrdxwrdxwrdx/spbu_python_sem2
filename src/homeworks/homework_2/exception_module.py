class IncorrectCollectionError(Exception):
    def __init__(self, collection_name: str, expected_collection_name: str = "Collection") -> None:
        self.collection_name = collection_name
        self.expected_collection_name = expected_collection_name
        super().__init__(
            f"Incompatible collection: expected subclass of {expected_collection_name}, got '{collection_name}'"
        )


class IncorrectActionError(Exception):
    def __init__(self, action_name: str) -> None:
        self.action_name = action_name
        super().__init__(f"No actions are named '{action_name}'")


class EmptyStorageError(Exception):
    def __init__(self) -> None:
        super().__init__(f"Storage is Empty")


class EmptyActionsError(Exception):
    def __init__(self) -> None:
        super().__init__(f"No actions to Undo")


class UnexpectedInverseAction(Exception):
    def __init__(self) -> None:
        super().__init__(f"Unexpectred inverse ation")
