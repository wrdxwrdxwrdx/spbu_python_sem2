import random
from collections.abc import MutableMapping
from typing import Generic, Iterator, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    def __init__(
        self,
        key: K,
        value: V,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        /,
        priority: float = None,
    ):
        self.left = left
        self.right = right
        self.key = key
        self.value = value
        if priority is None:
            priority = random.random()
        self.priority = priority

    def __str__(self) -> str:
        return f"[<{self.key}, {self.value}>, left={self.left}, right={self.right}]"

    def __repr__(self) -> str:
        return f"[<{self.key}, {self.value}, {self.priority}>, left={repr(self.left)}, right={repr(self.right)}]"


class Treap(MutableMapping, Generic[K, V]):
    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self.size: int = 0

    @staticmethod
    def merge_node(left_node: Optional[Node], right_node: Optional[Node]) -> Optional[Node]:
        if left_node is None:
            return right_node
        elif right_node is None:
            return left_node
        elif left_node.priority > right_node.priority:
            left_node.right = Treap.merge_node(left_node.right, right_node)
            return left_node
        else:
            right_node.left = Treap.merge_node(left_node, right_node.left)
            return right_node

    @staticmethod
    def split_node(root: Optional[Node], key: K) -> Tuple[Optional[Node], Optional[Node]]:
        if root is None:
            return None, None
        if key > root.key:
            left_treap, right_treap = Treap.split_node(root.right, key)
            root.right = left_treap
            return root, right_treap
        else:
            left_treap, right_treap = Treap.split_node(root.left, key)
            root.left = right_treap
            return left_treap, root

    def __delitem__(self, key: K) -> None:
        def delete(root: Optional[Node], key: K) -> Optional[Node]:
            if root is None:
                raise KeyError(f"No K({key}) in Treap")
            if key < root.key:
                root.left = delete(root.left, key)
            elif key > root.key:
                root.right = delete(root.right, key)
            else:
                return self.merge_node(root.left, root.right)
            return root

        self.root = delete(self.root, key)
        self.size -= 1

    def __getitem__(self, key: K) -> Optional[V]:
        def getitem(root: Optional[Node], key: K) -> Optional[V]:
            if root is not None:
                if root.key < key:
                    return getitem(root.right, key)
                elif root.key > key:
                    return getitem(root.left, key)
                else:
                    return root.value
            raise KeyError(f"No K({key}) in Treap")

        return getitem(self.root, key)

    def __iter__(self) -> Iterator[K]:
        def iterate(root: Optional[Node]) -> Iterator[K]:
            if root is not None:
                yield from iterate(root.left)
                yield root.key
                yield from iterate(root.right)

        return iterate(self.root)

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: K, value: V) -> None:
        if key in self:
            del self[key]
        left_node, right_node = self.split_node(self.root, key)
        new_node = Node(key, value)
        left_node = self.merge_node(left_node, new_node)
        self.root = self.merge_node(left_node, right_node)
        self.size += 1

    def __str__(self) -> str:
        root = self.root
        if root:
            return f"[<{root.key}, {root.value}>, left={root.left}, right={root.right}]"
        else:
            return "None"

    def __repr__(self) -> str:
        root = self.root
        if root:
            return f"[<{root.key}, {root.value}, {root.priority}>, left={repr(root.left)}, right={repr(root.right)}]"
        else:
            return "None"
