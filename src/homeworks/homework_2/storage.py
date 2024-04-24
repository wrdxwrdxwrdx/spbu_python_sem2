import random
from copy import copy
from typing import Collection, Generic, MutableSequence, Optional, Set, TypeVar

from typing_extensions import Any

from src.homeworks.homework_2.exception_module import *

C = TypeVar("C")


class Action:
    object_collection_type = object

    def action(self, object_collection: Any) -> Any:
        return NotImplementedError

    def inverse_action(self, object_collection: Any) -> Any:
        return NotImplementedError


class AddToStart(Action):
    object_collection_type = MutableSequence

    def __init__(self, number: int) -> None:
        self.number = number

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        object_collection.insert(0, self.number)
        return object_collection

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if len(object_collection) > 0:
            object_collection.pop(0)
            return object_collection
        else:
            raise EmptyStorageError()


class DeleteFromStart(Action):
    object_collection_type = MutableSequence

    def __init__(self) -> None:
        self.deleted_obj: Optional[int] = None

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if len(object_collection) > 0:
            self.deleted_obj = object_collection.pop(0)
            return object_collection
        else:
            raise EmptyStorageError()

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if self.deleted_obj is not None:
            object_collection.insert(0, self.deleted_obj)
            return object_collection
        else:
            raise UnexpectedInverseAction()


class AddToEnd(Action):
    object_collection_type = MutableSequence

    def __init__(self, number: int) -> None:
        self.number = number

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        object_collection.append(self.number)
        return object_collection

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if len(object_collection) > 0:
            object_collection.pop()
            return object_collection
        else:
            raise EmptyStorageError()


class DeleteFromEnd(Action):
    object_collection_type = MutableSequence

    def __init__(self) -> None:
        self.deleted_number: Optional[int] = None

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if len(object_collection) > 0:
            self.deleted_number = object_collection.pop()
            return object_collection
        else:
            raise EmptyStorageError()

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if self.deleted_number is not None:
            object_collection.append(self.deleted_number)
            return object_collection
        else:
            raise UnexpectedInverseAction()


class AddToSet(Action):
    object_collection_type = Set

    def __init__(self, number: int) -> None:
        self.number: Optional[int] = number

    def action(self, object_collection: Set[int]) -> Set[int]:
        if self.number in object_collection:
            self.number = None
        elif self.number is not None:
            object_collection.add(self.number)
        return object_collection

    def inverse_action(self, object_collection: Set[int]) -> Set[int]:
        if len(object_collection) > 0:
            if self.number is not None:
                object_collection.remove(self.number)
            return object_collection
        else:
            raise EmptyStorageError()


class DeleteFromSet(Action):
    object_collection_type = Set

    def __init__(self, number: int) -> None:
        self.number = number

    def action(self, object_collection: Set[int]) -> Set[int]:
        if self.number in object_collection:
            object_collection.remove(self.number)
            return object_collection
        else:
            raise ValueError(f"No element {self.number} in Storage")

    def inverse_action(self, object_collection: Set[int]) -> Set[int]:
        object_collection.add(self.number)
        return object_collection


class ChangeIndex(Action):
    object_collection_type = MutableSequence

    def __init__(self, first_index: int, second_index: int) -> None:
        self.first_index = first_index
        self.second_index = second_index

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if abs(self.first_index) < len(object_collection) and abs(self.second_index) < len(object_collection):
            object_collection.insert(self.second_index, object_collection.pop(self.first_index))
            return object_collection
        else:
            raise IndexError("Incorrect indexes")

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if abs(self.first_index) < len(object_collection) and abs(self.second_index) < len(object_collection):
            object_collection.insert(self.first_index, object_collection.pop(self.second_index))
            return object_collection
        else:
            raise IndexError("Incorrect indexes")


class AddValue(Action):
    object_collection_type = MutableSequence

    def __init__(self, index: int, number: int) -> None:
        self.index = index
        self.number = number

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] += self.number
            return object_collection
        else:
            raise IndexError("Incorrect indexes")

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] -= self.number
            return object_collection
        else:
            raise IndexError("Incorrect indexes")


class Reverse(Action):
    object_collection_type = MutableSequence

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        return object_collection[::-1]

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        return object_collection[::-1]


class MultiplyValue(Action):
    object_collection_type = MutableSequence

    def __init__(self, index: int, number: int) -> None:
        self.index = index
        self.value = number

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] *= self.value
            return object_collection
        else:
            raise IndexError("Incorrect indexes")

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if abs(self.index) < len(object_collection):
            object_collection[self.index] //= self.value
            return object_collection
        else:
            raise IndexError("Incorrect indexes")


class SortAscending(Action):
    object_collection_type = MutableSequence

    def __init__(self) -> None:
        self.unsorted_collection: Optional[MutableSequence[int]] = None

    @staticmethod
    def bubble_ascending(collection: MutableSequence[int]) -> MutableSequence[int]:
        for i in range(0, len(collection) - 1):
            for j in range(0, len(collection) - 1 - i):
                if collection[j] > collection[j + 1]:
                    collection[j], collection[j + 1] = collection[j + 1], collection[j]
        return collection

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        self.unsorted_collection = copy(object_collection)
        return self.bubble_ascending(object_collection)

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if self.unsorted_collection is not None:
            return self.unsorted_collection
        else:
            raise UnexpectedInverseAction()


class SortDescending(Action):
    object_collection_type = MutableSequence

    def __init__(self) -> None:
        self.unsorted_collection: Optional[MutableSequence[int]] = None

    @staticmethod
    def bubble_descending(collection: MutableSequence[int]) -> MutableSequence[int]:
        for i in range(0, len(collection) - 1):
            for j in range(0, len(collection) - 1 - i):
                if collection[j] < collection[j + 1]:
                    collection[j], collection[j + 1] = collection[j + 1], collection[j]
        return collection

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        self.unsorted_collection = copy(object_collection)
        return self.bubble_descending(object_collection)

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if self.unsorted_collection is not None:
            return self.unsorted_collection
        else:
            raise UnexpectedInverseAction()


class Shuffle(Action):
    object_collection_type = MutableSequence

    def __init__(self) -> None:
        self.unshuffled_collection: Optional[MutableSequence[int]] = None

    def action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        self.unshuffled_collection = copy(object_collection)
        random.shuffle(object_collection)
        return object_collection

    def inverse_action(self, object_collection: MutableSequence[int]) -> MutableSequence[int]:
        if self.unshuffled_collection is not None:
            return self.unshuffled_collection
        else:
            raise UnexpectedInverseAction()


class PerformedCommandStorage(Generic[C]):
    def __init__(self, collection: Collection[C]) -> None:
        self.collection = collection
        self.action_list: list[Action] = []

    def apply(self, action: Action) -> None:
        object_collection_type = type(self.collection)
        if issubclass(object_collection_type, action.object_collection_type):
            self.collection = action.action(self.collection)
            self.action_list.append(action)
        else:
            raise IncorrectCollectionError(
                object_collection_type.__name__, expected_collection_name=action.object_collection_type.__name__
            )

    def undo(self) -> None:
        if len(self.action_list) > 0:
            self.collection = self.action_list[-1].inverse_action(self.collection)
            self.action_list.pop()
        else:
            raise EmptyActionsError()
