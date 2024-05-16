from typing import Generic, Protocol, TypeVar


class ArithmeticAvailable(Protocol):
    def __add__(self, other: "ArithmeticAvailable") -> "ArithmeticAvailable":
        ...

    def __mul__(self, other: "ArithmeticAvailable") -> "ArithmeticAvailable":
        ...

    def __sub__(self, other: "ArithmeticAvailable") -> "ArithmeticAvailable":
        ...


T = TypeVar("T", bound=ArithmeticAvailable)


class Vector(Generic[T]):
    def __init__(self, coords: list[T]):
        self.coords = coords

    def __add__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise DimensionError(self, other)
        new_coords = []
        for i in range(len(self)):
            new_coords.append(self.coords[i] + other.coords[i])
        return Vector(new_coords)

    def __sub__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise DimensionError(self, other)
        new_coords = []
        for i in range(len(self)):
            new_coords.append(self.coords[i] - other.coords[i])
        return Vector(new_coords)

    def __mul__(self, other: "Vector") -> "Vector":
        if len(self) != 3:
            raise ExpectedDimensionError(self, 3)
        if len(other) != 3:
            raise ExpectedDimensionError(other, 3)
        a1, a2, a3 = self.coords
        b1, b2, b3 = other.coords
        s1 = a2 * b3 - a3 * b2
        s2 = a3 * b1 - a1 * b3
        s3 = a1 * b2 - a2 * b1
        return Vector([s1, s2, s3])

    @staticmethod
    def scalar_product(vector_1: "Vector", vector_2: "Vector") -> T:
        if len(vector_1) != len(vector_2):
            raise DimensionError(vector_1, vector_2)
        return sum(vector_1.coords[i] * vector_2.coords[i] for i in range(len(vector_1)))

    def is_null(self) -> bool:
        return not any(self.coords)

    def __str__(self) -> str:
        return "<" + ", ".join(map(str, self.coords)) + ">"

    def __repr__(self) -> str:
        return f"dim={len(self)} " + "<" + ", ".join(map(str, self.coords)) + ">"

    def __len__(self) -> int:
        return len(self.coords)


class DimensionError(Exception):
    def __init__(self, vector_1: Vector, vector_2: Vector) -> None:
        super().__init__(
            f"Vectors must be the same dimension. Dimension of {vector_1} is {len(vector_1.coords)}, but dimension of {vector_2} is {len(vector_2.coords)},"
        )


class ExpectedDimensionError(Exception):
    def __init__(self, vector: Vector, expected_dimension: int) -> None:
        super().__init__(
            f"Vectors must be {expected_dimension} dimension. Dimension of {vector} is {len(vector.coords)}, but must be {expected_dimension}"
        )
