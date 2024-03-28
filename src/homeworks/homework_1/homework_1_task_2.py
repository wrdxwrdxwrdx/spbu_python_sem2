import random
from collections.abc import MutableMapping
from typing import Generic, Iterable, Iterator, Optional, Set, Tuple, TypeVar

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
        if priority:
            self.priority = priority
        else:
            self.priority = random.random()

    def __str__(self) -> str:
        if self:
            return f"[<{self.key}, {self.value}>, left={self.left}, right={self.right}]"
        else:
            return "None"

    def __repr__(self) -> str:
        if self:
            return f"[<{self.key}, {self.value}, {self.priority}>, left={self.left.__repr__()}, right={self.right.__repr__()}]"
        else:
            return "None"


class Treap(MutableMapping):
    def __init__(self, root: Node = None, size: int = 0):
        self.root = root
        self.size = size

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
        def iterate(root: Optional[Node], output: Set[K]) -> Set[K]:
            if root is not None:
                output.add(root.key)
                output = iterate(root.left, output)
                output = iterate(root.right, output)
            return output

        return iter(iterate(self.root, set()))

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: K, value: V) -> None:
        def update(__m: Iterable[Tuple[K, V]]) -> None:
            def _update(root: Optional[Node], key: K, value: V) -> Optional[Node]:
                if root is None:
                    return root
                if key == root.key:
                    root.value = value
                    return root
                if root is not None and key < root.key:
                    root.left = _update(root.left, key, value)
                    return root
                if root is not None and key > root.key:
                    root.right = _update(root.right, key, value)
                    return root

            for key, value in __m:
                self.root = _update(self.root, key, value)

        if self.root:
            if key in self:
                update(((key, value),))
            left_treap, right_treap = self.split_node(self.root, key)
            new_element: Node = Node(key, value)
            left_treap = self.merge_node(left_treap, new_element)
            self.root = self.merge_node(left_treap, right_treap)
        else:
            self.root = Node(key, value)

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
            return f"[<{root.key}, {root.value}, {root.priority}>, left={root.left.__repr__()}, right={root.right.__repr__()}]"
        else:
            return "None"
