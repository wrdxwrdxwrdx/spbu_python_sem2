import pytest

from src.exam.exam_1.exam_1_task_2 import *


class TestVector:
    @pytest.mark.parametrize(
        "coords_1, coords_2, expected",
        (
            ([0, 0, 1], [1, 1, 0], [1, 1, 1]),
            ([-1, 4, 1], [1, 1, 0], [0, 5, 1]),
            ([12, 0.5, -3], [-2, 1, -7], [10, 1.5, -10]),
            ([-1, -2.5, -3], [1, 2, 32.5], [0, -0.5, 29.5]),
        ),
    )
    def test_add(self, coords_1, coords_2, expected):
        vector_1 = Vector(coords_1)
        vector_2 = Vector(coords_2)
        assert (vector_1 + vector_2).coords == expected

    @pytest.mark.parametrize(
        "coords_1, coords_2, expected",
        (
            ([0, 0, 1], [1, 1, 0], [-1, -1, 1]),
            ([-1, 4, 1], [1, 1, 0], [-2, 3, 1]),
            ([12, 0.5, -3], [-2, 1, -7], [14, -0.5, 4]),
            ([-1, -2.5, -3], [1, 2, 32.5], [-2, -4.5, -35.5]),
        ),
    )
    def test_sub(self, coords_1, coords_2, expected):
        vector_1 = Vector(coords_1)
        vector_2 = Vector(coords_2)
        assert (vector_1 - vector_2).coords == expected

    @pytest.mark.parametrize(
        "coords_1, coords_2, expected",
        (
            ([0, 0, 1], [1, 1, 0], [-1, 1, 0]),
            ([-1, 4, 1], [1, 1, 0], [-1, 1, -5]),
            ([12, 0.5, -3], [-2, 1, -7], [-0.5, 90, 13.0]),
            ([-1, -2.5, -3], [1, 2, 32.5], [-75.25, 29.5, 0.5]),
        ),
    )
    def test_mul(self, coords_1, coords_2, expected):
        vector_1 = Vector(coords_1)
        vector_2 = Vector(coords_2)
        assert (vector_1 * vector_2).coords == expected

    @pytest.mark.parametrize(
        "coords_1, coords_2, expected",
        (
            ([0, 0, 1], [1, 1, 0], 0),
            ([-1, 4, 1], [1, 1, 0], 3),
            ([12, 0.5, -3], [-2, 1, -7], -2.5),
            ([-1, -2.5, -3], [1, 2, 32.5], -103.5),
        ),
    )
    def test_mul(self, coords_1, coords_2, expected):
        vector_1 = Vector(coords_1)
        vector_2 = Vector(coords_2)
        assert Vector.scalar_product(vector_1, vector_2) == expected

    @pytest.mark.parametrize("coords_1, expected", (([0, 0, 1], False), ([0, 0, 0], True)))
    def test_null(self, coords_1, expected):
        vector_1 = Vector(coords_1)
        assert vector_1.is_null() == expected

    @pytest.mark.parametrize("coords_1, expected", (([0, 0, 1], 3), ([0, 0], 2)))
    def test_len(self, coords_1, expected):
        vector_1 = Vector(coords_1)
        assert len(vector_1) == expected

    @pytest.mark.parametrize("coords", (([0, 0, 1]), ([-1, 4, 1]), ([12, 0.5, -3, -7]), ([-1, -2.5, 1, 2, 32.5])))
    def test_str(self, coords):
        vector = Vector(coords)
        assert str(vector) == "<" + ", ".join(map(str, coords)) + ">"

    @pytest.mark.parametrize("coords", (([0, 0, 1]), ([-1, 4, 1]), ([12, 0.5, -3, -7]), ([-1, -2.5, 1, 2, 32.5])))
    def test_str(self, coords):
        vector = Vector(coords)
        assert repr(vector) == f"dim={len(coords)} " + "<" + ", ".join(map(str, coords)) + ">"

    def test_exception_add(self):
        with pytest.raises(DimensionError):
            vector_1 = Vector([1, 2])
            vector_2 = Vector([1, 2, 3])
            v = vector_1 + vector_2

    def test_exception_sub(self):
        with pytest.raises(DimensionError):
            vector_1 = Vector([1, 2])
            vector_2 = Vector([1, 2, 3])
            v = vector_1 - vector_2

    def test_exception_mul(self):
        with pytest.raises(ExpectedDimensionError):
            vector_1 = Vector([1, 2, 1, 12])
            vector_2 = Vector([1, 2, 3, 2])
            v = vector_1 * vector_2

    def test_exception_scalar_product(self):
        with pytest.raises(DimensionError):
            vector_1 = Vector([1, 2])
            vector_2 = Vector([1, 2, 3])
            Vector.scalar_product(vector_1, vector_2)
