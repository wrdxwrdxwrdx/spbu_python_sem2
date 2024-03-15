import pytest

from src.homeworks.homework_1.homework_1_task_2 import *

Key = int
Value = int


def create_treap(items: Tuple[Tuple[Key, Value], ...]) -> Treap:
    treap = Treap()
    for key, value in items:
        treap[key] = value
    return treap


def test_len():
    for length in range(1, 25):
        treap = Treap()
        for i in range(1, length + 1):
            treap[i] = i
            assert len(treap) == i
        for i in range(1, length + 1):
            treap.popitem()
            assert len(treap) == length - i


@pytest.mark.parametrize(
    "items,del_item", [(((1, 1), (2, 2)), (1, 1)), (((1, 1), (2, 2)), (2, 2)), (((1, 1), (2, 2), (3, 3)), (2, 2))]
)
def test_delitem(items, del_item):
    treap = create_treap(items)
    treap_start_size = len(items)
    del treap[del_item[0]]
    assert del_item not in list(treap.items()) and treap_start_size == len(items)


@pytest.mark.parametrize(
    "items,del_item", [(((1, 1), (2, 2)), (10, 1)), (((1, 1), (2, 2)), (20, 2)), (((1, 1), (2, 2), (3, 3)), (20, 2))]
)
def test_delitem_exception(items, del_item):
    treap = create_treap(items)
    with pytest.raises(KeyError):
        del treap[del_item[0]]


@pytest.mark.parametrize(
    "items", [((1, 1), (2, 2)), ((1, 1), (2, 2)), ((1, 1), (2, 2), (3, 3)), ((1, 12), (12, 2), (98, 23))]
)
def test_getitem(items):
    treap = create_treap(items)
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
def test_getitem_exception(items, exception_key):
    treap = create_treap(items)
    with pytest.raises(KeyError):
        assert treap[exception_key]


@pytest.mark.parametrize(
    "items,expected_items",
    [
        (((1, 1), (2, 2)), ((1, 1), (2, 2))),
        (((1, 1), (2, 2), (3, 3)), ((1, 1), (2, 2), (3, 3))),
        (((1, 12), (12, 2), (98, 23), (1, 1)), ((12, 2), (98, 23), (1, 1))),
    ],
)
def test_setitem(items, expected_items):
    treap = create_treap(items)
    for key, value in expected_items:
        assert treap[key] == value


@pytest.mark.parametrize(
    "items_1,items_2,expected",
    [
        (((1, 1), (2, 2)), ((1, 1), (2, 2)), True),
        (((1, 1), (2, 2), (3, 3)), ((1, 1), (2, 2), (3, 2)), False),
        (((12, 2), (98, 23), (1, 1)), ((12, 2), (98, 23), (1, 1)), True),
    ],
)
def test_eq(items_1, items_2, expected):
    treap_1 = create_treap(items_1)
    treap_2 = create_treap(items_2)
    assert (treap_1 == treap_2) == expected


@pytest.mark.parametrize(
    "items,not_treap",
    [
        (((1, 1), (2, 2)), 5),
        (((1, 1), (2, 2), (3, 3)), "123"),
        (((12, 2), (98, 23), (1, 1)), 1.23),
    ],
)
def test_eq_exception(items, not_treap):
    treap = create_treap(items)
    with pytest.raises(NotImplementedError):
        assert treap == not_treap


@pytest.mark.parametrize(
    "items",
    [((1, 1), (2, 2)), ((1, 1), (2, 2), (3, 3)), ((1, 12), (12, 2), (98, 23), (1, 1))],
)
def test_iter(items):
    treap = create_treap(items)
    iter_list = list(treap.__iter__())
    assert iter_list == list(treap.keys())


@pytest.mark.parametrize(
    "items,string",
    [
        (((1, 1), (2, 2)), "[<2, 2>, left=[<1, 1>, left=None, right=None], right=None]"),
        (
            ((1, 1), (2, 2), (3, 3)),
            "[<3, 3>, left=[<2, 2>, left=[<1, 1>, left=None, right=None], right=None], right=None]",
        ),
        (
            ((1, 12), (12, 2), (98, 23), (1, 1)),
            "[<98, 23>, left=[<12, 2>, left=[<1, 1>, left=[<1, 1>, left=None, right=None], right=None], right=None], right=None]",
        ),
    ],
)
def test_str(items, string):
    treap = create_treap(items)
    assert str(treap) == string


@pytest.mark.parametrize(
    "items,key",
    [(((1, 1), (2, 2)), 1), (((1, 1), (2, 2), (3, 3)), 2), (((1, 12), (12, 2), (98, 23), (1, 1)), 12)],
)
def test_split(items, key):
    treap = create_treap(items)
    left, right = treap.split_node(treap.root, key)
    left_treap, right_treap = Treap(), Treap()
    left_treap.root, right_treap.root = left, right
    for left_treap_key in left_treap:
        assert left_treap_key < key
    for right_treap_key in right_treap:
        assert right_treap_key >= key


@pytest.mark.parametrize(
    "items,key",
    [(((1, 1), (2, 2)), 1), (((1, 1), (2, 2), (3, 3)), 2), (((1, 12), (12, 2), (98, 23), (1, 1)), 12)],
)
def test_merge(items, key):
    treap = create_treap(items)
    left, right = treap.split_node(treap.root, key)
    merged_treap = Treap()
    merged_treap.root = Treap.merge_node(left, right)
    assert treap == merged_treap
