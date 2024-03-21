import pytest

from src.homeworks.homework_1.homework_1_task_2 import *


class TestTreap:
    @staticmethod
    def create_random_items(size) -> tuple[tuple[Key, Value]]:
        keys = list(range(size))
        values = list(range(size))
        random.shuffle(values)
        random.shuffle(keys)
        items = zip(keys, values)
        return tuple(items)

    @staticmethod
    def create_treap(items: Tuple[Tuple[Key, Value], ...]) -> Treap:
        treap = Treap()
        for key, value in items:
            treap[key] = value
        return treap

    def test_len(self):
        for length in range(1, 25):
            treap = Treap()
            for i in range(1, length + 1):
                treap[i] = i
                assert len(treap) == i

    @pytest.mark.parametrize("size", [1, 2, 5, 10, 100])
    def test_delitem(self, size):
        treap = TestTreap.create_treap(zip(range(size), range(size)))
        random_keys = list(treap.keys())
        random.shuffle(random_keys)
        for key in random_keys:
            del treap[key]
            assert key not in treap

    @pytest.mark.parametrize(
        "items,del_item",
        [(((1, 1), (2, 2)), (10, 1)), (((1, 1), (2, 2)), (20, 2)), (((1, 1), (2, 2), (3, 3)), (20, 2))],
    )
    def test_delitem_exception(self, items, del_item):
        treap = TestTreap.create_treap(items)
        with pytest.raises(KeyError):
            del treap[del_item[0]]

    @pytest.mark.parametrize("size", [1, 2, 5, 10, 100])
    def test_getitem(self, size):
        items = TestTreap.create_random_items(size)
        treap = TestTreap.create_treap(items)
        for key, value in items:
            assert treap[key] == value

    @pytest.mark.parametrize(
        "items,exception_key",
        [
            (((1, 1), (2, 2)), 12),
            (((1, 1), (2, 2)), 15),
            (((1, 1), (2, 2), (3, 3)), 0),
            (((1, 12), (12, 2), (98, 23)), 123),
        ],
    )
    def test_getitem_exception(self, items, exception_key):
        treap = TestTreap.create_treap(items)
        with pytest.raises(KeyError):
            assert treap[exception_key]

    @pytest.mark.parametrize(
        "size",
        [1, 2, 3, 5, 10, 100],
    )
    def test_setitem(self, size):
        items = TestTreap.create_random_items(size)

        treap = Treap()
        for key, value in items:
            treap[key] = value
            assert treap[key] == value

    @pytest.mark.parametrize(
        "size",
        [1, 2, 3, 5, 10, 100],
    )
    def test_iter(self, size):
        items = TestTreap.create_random_items(size)
        treap = TestTreap.create_treap(items)
        iter_list = list(treap.__iter__())
        assert iter_list == list(treap.keys())

    @pytest.mark.parametrize(
        "size",
        [1, 2, 3, 5, 10, 100],
    )
    def test_split(self, size):
        items = TestTreap.create_random_items(size)
        key = random.randint(0, size)
        treap = TestTreap.create_treap(items)
        left, right = treap.split_node(treap.root, key)
        left_treap, right_treap = Treap(), Treap()
        left_treap.root, right_treap.root = left, right
        for left_treap_key in left_treap:
            assert left_treap_key < key
        for right_treap_key in right_treap:
            assert right_treap_key >= key

    @pytest.mark.parametrize(
        "size",
        [1, 2, 3, 5, 10, 100],
    )
    def test_merge(self, size):
        items = TestTreap.create_random_items(size)
        key = random.randint(0, size)
        treap = TestTreap.create_treap(items)
        left, right = treap.split_node(treap.root, key)
        merged_treap = Treap()
        merged_treap.root = Treap.merge_node(left, right)
        assert treap == merged_treap
