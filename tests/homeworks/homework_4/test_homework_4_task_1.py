import random

import hypothesis.strategies as st
from hypothesis import given

from src.homeworks.homework_4.sorting_module import *


class TestSortingModule:
    @given(st.integers(100, 110))
    def test_merge_sort(self, length):
        array = [random.randint(-100, 100) for _ in range(length)]
        merge_sorted = merge_sort(array)
        assert merge_sorted == list(sorted(array))

    @given(st.integers(100, 1000), st.integers(1, 100))
    def test_thread_sort(self, length, thread_number):
        array = [random.randint(-100, 100) for _ in range(length)]
        thread_sorted = thread_sort(array, thread_number)
        assert thread_sorted == list(sorted(array))

    @given(st.integers(100, 1000), st.integers(1, 8))
    def test_process_sort(self, length, thread_number):
        array = [random.randint(-100, 100) for _ in range(length)]
        process_sorted = thread_sort(array, thread_number, multiprocess=True)
        assert process_sorted == list(sorted(array))

    @given(st.integers(1, 100), st.integers(1, 100))
    def test_split_array(self, length, part_number):
        array = [random.randint(-100, 100) for _ in range(length)]
        splitted_array = split_array(array, part_number)
        if part_number > len(array):
            assert len(splitted_array) == len(array)
        else:
            assert len(splitted_array) == part_number

        new_array = []
        for i in splitted_array:
            new_array += i
        assert new_array == array

    @given(st.integers(1, 100))
    def test_split_array(self, length):
        array_1 = [random.randint(-100, 100) for _ in range(length)]
        array_2 = [random.randint(-100, 100) for _ in range(length)]
        array_1.sort()
        array_2.sort()
        connected_array = array_1 + array_2
        connected_array.sort()
        assert connected_array == connect_arrays(array_1, array_2)
