from abc import ABCMeta


class StorageException(Exception, metaclass=ABCMeta):
    pass


class IncorrectActionError(StorageException):
    def __init__(self, action_name: str) -> None:
        self.action_name = action_name
        super().__init__(f"No actions are named '{action_name}'")


class EmptyStorageError(StorageException):
    def __init__(self) -> None:
        super().__init__(f"Storage is Empty")


class EmptyActionsError(StorageException):
    def __init__(self) -> None:
        super().__init__(f"No actions to Undo")


class UnexpectedInverseAction(StorageException):
    def __init__(self) -> None:
        super().__init__(f"Unexpectred inverse ation")
