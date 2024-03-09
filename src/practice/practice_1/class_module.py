from typing import TypeVar

Object = TypeVar("Object")


class Action:
    def action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        raise NotImplementedError

    def inverse_action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        raise NotImplementedError


class AddToStart(Action):
    def __init__(self, obj: Object):
        self.obj = obj

    def action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        object_list.insert(0, self.obj)
        return object_list

    def inverse_action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        if len(object_list) > 0:
            object_list.pop(0)
            return object_list


class AddToEnd(Action):
    def __init__(self, obj: Object):
        self.obj = obj

    def action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        object_list.append(self.obj)
        return object_list

    def inverse_action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        if len(object_list) > 0:
            object_list.pop()
            return object_list
        else:
            raise ValueError("Storage is Empty")


class ChangeIndex(Action):
    def __init__(self, first_index: int, second_index: int):
        self.first_index = first_index
        self.second_index = second_index

    def action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        if abs(self.first_index) < len(object_list) and abs(self.second_index) < len(object_list):
            object_list.insert(self.second_index, object_list.pop(self.first_index))
            return object_list
        else:
            raise ValueError("Incorrect indexes")

    def inverse_action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        if abs(self.first_index) < len(object_list) and abs(self.second_index) < len(object_list):
            object_list.insert(self.first_index, object_list.pop(self.second_index))
            return object_list
        else:
            raise ValueError("Incorrect indexes")


class AddValue(Action):
    def __init__(self, index: int, value: Object):
        self.index = index
        self.value = value

    def action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        if abs(self.index) < len(object_list):
            object_list[self.index] += self.value
            return object_list
        else:
            raise ValueError("Incorrect indexes")

    def inverse_action(self, object_list: list[Object, ...]) -> list[Object, ...]:
        if abs(self.index) < len(object_list):
            object_list[self.index] -= self.value
            return object_list

        raise ValueError("Incorrect indexes")


class PerformedCommandStorage:
    def __init__(self, object_list):
        self.object_list = object_list
        self.action_list = []

    def apply(self, action: Action):
        self.object_list = action.action(self.object_list)
        self.action_list.append(action)

    def undo(self):
        if len(self.action_list) > 0:
            self.object_list = self.action_list[-1].inverse_action(self.object_list)
            self.action_list.pop()
        else:
            raise ValueError("Action list is empty")

    def get_storage(self):
        return self.object_list

    def get_actions(self):
        return self.action_list
