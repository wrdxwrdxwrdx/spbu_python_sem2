import abc
import random
from copy import copy
from typing import Collection, Generic, Optional, TypeVar

from src.homeworks.homework_1.homework_1_task_1 import Registry
from src.homeworks.homework_2.storage_exceptions import *


class Action:
    @abc.abstractmethod
    def action(self, object_collection: list[int]) -> list[int]:
        ...

    @abc.abstractmethod
    def inverse_action(self, object_collection: list[int]) -> list[int]:
        ...


registry = Registry[Action](default=None)


@registry.register("AddToStart")
class AddToStart(Action):
    def __init__(self, number: int) -> None:
        self.number = number

    def action(self, object_collection: list[int]) -> list[int]:
        object_collection.insert(0, self.number)
        return object_collection

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if len(object_collection) > 0:
            object_collection.pop(0)
            return object_collection
        else:
            raise EmptyStorageError()


@registry.register("DeleteFromStart")
class DeleteFromStart(Action):
    def __init__(self) -> None:
        self.deleted_obj: Optional[int] = None

    def action(self, object_collection: list[int]) -> list[int]:
        if len(object_collection) > 0:
            self.deleted_obj = object_collection.pop(0)
            return object_collection
        else:
            raise EmptyStorageError()

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if self.deleted_obj is not None:
            object_collection.insert(0, self.deleted_obj)
            return object_collection
        else:
            raise UnexpectedInverseAction()


@registry.register("AddToEnd")
class AddToEnd(Action):
    def __init__(self, number: int) -> None:
        self.number = number

    def action(self, object_collection: list[int]) -> list[int]:
        object_collection.append(self.number)
        return object_collection

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if len(object_collection) > 0:
            object_collection.pop()
            return object_collection
        else:
            raise EmptyStorageError()


@registry.register("DeleteFromEnd")
class DeleteFromEnd(Action):
    def __init__(self) -> None:
        self.deleted_number: Optional[int] = None

    def action(self, object_collection: list[int]) -> list[int]:
        if len(object_collection) > 0:
            self.deleted_number = object_collection.pop()
            return object_collection
        else:
            raise EmptyStorageError()

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if self.deleted_number is not None:
            object_collection.append(self.deleted_number)
            return object_collection
        else:
            raise UnexpectedInverseAction()


@registry.register("ChangeIndex")
class ChangeIndex(Action):
    def __init__(self, first_index: int, second_index: int) -> None:
        self.first_index = first_index
        self.second_index = second_index

    def action(self, object_collection: list[int]) -> list[int]:
        if abs(self.first_index) < len(object_collection) and abs(self.second_index) < len(object_collection):
            object_collection.insert(self.second_index, object_collection.pop(self.first_index))
            return object_collection
        else:
            raise IndexError("Incorrect indexes")

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if abs(self.first_index) < len(object_collection) and abs(self.second_index) < len(object_collection):
            object_collection.insert(self.first_index, object_collection.pop(self.second_index))
            return object_collection
        else:
            raise IndexError("Incorrect indexes")


@registry.register("AddValue")
class AddValue(Action):
    def __init__(self, index: int, number: int) -> None:
        self.index = index
        self.number = number

    def action(self, object_collection: list[int]) -> list[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] += self.number
            return object_collection
        else:
            raise IndexError("Incorrect indexes")

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] -= self.number
            return object_collection
        else:
            raise IndexError("Incorrect indexes")


@registry.register("Reverse")
class Reverse(Action):
    def action(self, object_collection: list[int]) -> list[int]:
        return object_collection[::-1]

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        return object_collection[::-1]


@registry.register("MultiplyValue")
class MultiplyValue(Action):
    def __init__(self, index: int, number: int) -> None:
        self.index = index
        self.value = number

    def action(self, object_collection: list[int]) -> list[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] *= self.value
            return object_collection
        else:
            raise IndexError("Incorrect indexes")

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] //= self.value
            return object_collection
        else:
            raise IndexError("Incorrect indexes")


@registry.register("SortAscending")
class SortAscending(Action):
    def __init__(self) -> None:
        self.unsorted_collection: Optional[list[int]] = None

    def action(self, object_collection: list[int]) -> list[int]:
        self.unsorted_collection = copy(object_collection)
        object_collection.sort()
        return object_collection

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if self.unsorted_collection is not None:
            return self.unsorted_collection
        else:
            raise UnexpectedInverseAction()


@registry.register("SortDescending")
class SortDescending(Action):
    def __init__(self) -> None:
        self.unsorted_collection: Optional[list[int]] = None

    def action(self, object_collection: list[int]) -> list[int]:
        self.unsorted_collection = copy(object_collection)
        object_collection.sort(reverse=True)
        return object_collection

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if self.unsorted_collection is not None:
            return self.unsorted_collection
        else:
            raise UnexpectedInverseAction()


@registry.register("Shuffle")
class Shuffle(Action):
    def __init__(self) -> None:
        self.unshuffled_collection: Optional[list[int]] = None

    def action(self, object_collection: list[int]) -> list[int]:
        self.unshuffled_collection = copy(object_collection)
        random.shuffle(object_collection)
        return object_collection

    def inverse_action(self, object_collection: list[int]) -> list[int]:
        if self.unshuffled_collection is not None:
            return self.unshuffled_collection
        else:
            raise UnexpectedInverseAction()


class PerformedCommandStorage:
    def __init__(self, collection: list[int]) -> None:
        self.collection = collection
        self.action_list: list[Action] = []

    def apply(self, action: Action) -> None:
        self.collection = action.action(self.collection)
        self.action_list.append(action)

    def undo(self) -> None:
        if len(self.action_list) > 0:
            self.collection = self.action_list[-1].inverse_action(self.collection)
            self.action_list.pop()
        else:
            raise EmptyActionsError()
