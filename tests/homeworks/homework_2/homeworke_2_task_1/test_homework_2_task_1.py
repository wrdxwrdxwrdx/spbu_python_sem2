from io import StringIO

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.homeworks.homework_2.homework_2_task_1 import *


class TestAction:
    @given(st.integers(1, 100))
    def test_add_to_start(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        number = random.randint(-100, 100)
        action = AddToStart(number)
        assert action.action(collection) == [number, *collection_copy]
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_add_to_end(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        number = random.randint(-100, 100)
        action = AddToEnd(number)
        assert action.action(collection) == [*collection_copy, number]
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_delete_from_start(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        action = DeleteFromStart()
        assert action.action(collection) == collection_copy[1:]
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_delete_from_end(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        action = DeleteFromEnd()
        assert action.action(collection) == collection_copy[:-1]
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_change_index(self, collection_length):
        collection = list(random.randint(-100, 100) for _ in range(collection_length))
        collection_copy = copy(collection)
        first_index, second_index = random.randint(0, collection_length - 1), random.randint(0, collection_length - 1)

        action = ChangeIndex(first_index, second_index)
        collection_copy.insert(second_index, collection_copy.pop(first_index))
        assert action.action(collection) == collection_copy
        collection_copy.insert(first_index, collection_copy.pop(second_index))
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_add_value(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        index, value = random.randint(0, collection_length - 1), random.randint(-100, 100)
        action = AddValue(index, value)
        collection_copy[index] += value
        assert action.action(collection) == collection_copy
        collection_copy[index] -= value
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_reverse(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        action = Reverse()
        reverse_collection = action.action(collection)
        assert reverse_collection == collection_copy[::-1]
        assert action.inverse_action(reverse_collection) == collection_copy

    @given(st.integers(1, 100))
    def test_multiply_value(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        multiply_collection = copy(collection)
        index, value = random.randint(0, collection_length - 1), random.randint(-100, 100)
        action = MultiplyValue(index, value)
        multiply_collection[index] *= value
        assert action.action(collection) == multiply_collection
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_sort_ascending(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        collection_sorted_copy = copy(collection)
        action = SortAscending()
        collection_sorted_copy.sort()
        assert action.action(collection) == collection_sorted_copy
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(1, 100))
    def test_sort_descending(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        collection_sorted_copy = copy(collection)
        action = SortDescending()
        collection_sorted_copy.sort(reverse=True)
        assert action.action(collection) == collection_sorted_copy
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(2, 100))
    def test_sort_descending(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        collection_sorted_copy = copy(collection)
        action = SortDescending()
        collection_sorted_copy.sort(reverse=True)
        assert action.action(collection) == collection_sorted_copy
        assert action.inverse_action(collection) == collection_copy

    @given(st.integers(3, 100))
    def test_shuffle(self, collection_length):
        collection = [random.randint(-100, 100) for _ in range(collection_length)]
        collection_copy = copy(collection)
        for i in range(10):
            collection = copy(collection_copy)
            action = Shuffle()
            shuffled_collection = action.action(collection)
            if shuffled_collection != collection_copy:
                assert shuffled_collection != collection_copy
                assert action.inverse_action(shuffled_collection) == collection_copy
                break

    def test_add_to_start_error(self):
        action = AddToStart(1)

        with pytest.raises(EmptyStorageError):
            action.inverse_action([])

    def test_delete_from_start_error(self):
        action = DeleteFromStart()
        with pytest.raises(EmptyStorageError):
            action.action([])
        with pytest.raises(UnexpectedInverseAction):
            action.inverse_action([])

    def test_add_to_end_error(self):
        with pytest.raises(EmptyStorageError):
            action = AddToEnd(1)
            action.inverse_action([])

    def test_delete_from_end_error(self):
        with pytest.raises(EmptyStorageError):
            action = DeleteFromEnd()
            action.action([])
        with pytest.raises(UnexpectedInverseAction):
            action = DeleteFromEnd()
            action.inverse_action([])

    def test_change_index_error(self):
        with pytest.raises(IndexError):
            action = ChangeIndex(-10, 6)
            action.action([1, 2, 3])
        with pytest.raises(IndexError):
            action = ChangeIndex(-10, 6)
            action.inverse_action([1, 2, 3])

    def test_add_value_error(self):
        with pytest.raises(IndexError):
            action = AddValue(-10, 6)
            action.action([1, 2, 3])
        with pytest.raises(IndexError):
            action = AddValue(-10, 6)
            action.inverse_action([1, 2, 3])

    def test_multiply_value_error(self):
        with pytest.raises(IndexError):
            action = MultiplyValue(-10, 6)
            action.action([1, 2, 3])
        with pytest.raises(IndexError):
            action = MultiplyValue(-10, 6)
            action.inverse_action([1, 2, 3])

    def test_sort_ascending_error(self):
        with pytest.raises(UnexpectedInverseAction):
            action = SortAscending()
            action.inverse_action([1, 2, 3])

    def test_sort_descending_error(self):
        with pytest.raises(UnexpectedInverseAction):
            action = SortDescending()
            action.inverse_action([1, 2, 3])

    def test_shuffle_error(self):
        with pytest.raises(UnexpectedInverseAction):
            action = Shuffle()
            action.inverse_action([1, 2, 3])


class TestStorage:
    COMMAND_EXPLANATION = (
        "\nEnter command (AddToStart, AddToEnd, ChangeIndex, AddValue, ...) and args with space.\n"
        "Enter 'Undo' to cancel action.\n"
        "To exit enter 'q'.\n"
        "To see Object Collection enter 'Collection'.\n"
        "To see Full Command List enter 'Commands'.\n"
        "for example: 'ChangeIndex 2 3': \n"
    )

    def get_func_args_mutable_sequence(
        self, commands_annotation: dict[str, list[str]], command: str, storage_length: int
    ):
        args = []
        for argument in commands_annotation[command]:
            if argument == "number":
                args.append(random.randint(-100, 100))
            elif "index" in argument:
                args.append(random.randint(0, storage_length - 1))
        return args

    @given(st.integers(1, 100))
    def test_storage_mutable_sequence(self, command_number):
        action_registry = registry
        all_commands = list(action_registry.classes.keys())
        collection = [random.randint(-100, 100) for _ in range(100)]
        storage = PerformedCommandStorage[Action](copy(collection))

        available_commands_annotation = {}
        for command in all_commands:
            action = action_registry.dispatch(command)
            available_commands_annotation[command] = getfullargspec(action.__init__).args[1:]

        for _ in range(command_number):
            if len(storage.collection) == 0:
                break
            command = random.choice(list(available_commands_annotation.keys()))
            action = action_registry.dispatch(command)
            args = self.get_func_args_mutable_sequence(available_commands_annotation, command, len(storage.collection))
            storage.apply(action(*args))

        while len(storage.action_list):
            storage.undo()
        assert storage.collection == collection

    @pytest.mark.parametrize(
        "user_input, expected_output",
        [
            (
                ["1 2 3", "q"],
                [
                    "",
                ],
            ),
            (
                ["1 2 3", "AddToStart 0", "Collection", "q"],
                [
                    "\n[0, 1, 2, 3]",
                ],
            ),
            (["1 2 3", "AddToStart 0", "Collection", "Collection", "q"], ["\n[0, 1, 2, 3]", "[0, 1, 2, 3]"]),
            (
                ["1 2 3", "AddToStart 0", "Collection", "DeleteFromStart", "Collection", "q"],
                ["\n[0, 1, 2, 3]", "[1, 2, 3]"],
            ),
            (
                [
                    "1 2 3",
                    "AddToStart 0",
                    "Collection",
                    "DeleteFromStart",
                    "Collection",
                    "Undo",
                    "Collection",
                    "q",
                ],
                ["\n[0, 1, 2, 3]", "[1, 2, 3]", "[0, 1, 2, 3]"],
            ),
        ],
    )
    def test_main(self, monkeypatch, user_input, expected_output) -> None:
        monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
        fake_output = StringIO()
        monkeypatch.setattr("sys.stdout", fake_output)
        main()
        output = fake_output.getvalue()
        assert output == self.COMMAND_EXPLANATION + "\n".join(expected_output) + "\n"

    @pytest.mark.parametrize(
        "user_input, exception_text",
        [
            (["1 2 3", "Hello 1", "q"], "No actions are named 'Hello'"),
            (["1 2 3", "AddToStart World", "q"], "Expected int argument, got str"),
            (["", "DeleteFromStart", "q"], "Storage is Empty"),
            (["1 2 3", "Undo", "q"], "No actions to Undo"),
        ],
    )
    def test_main_error(self, monkeypatch, user_input, exception_text) -> None:
        monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
        fake_output = StringIO()
        monkeypatch.setattr("sys.stdout", fake_output)
        main()
        output = fake_output.getvalue()
        assert exception_text in output
