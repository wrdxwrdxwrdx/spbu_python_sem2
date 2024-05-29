from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def merge_sort(array: list[int]) -> list[int]:
    if len(array) <= 1:
        return array
    mid_pointer = len(array) // 2
    return connect_arrays(merge_sort(array[:mid_pointer]), merge_sort(array[mid_pointer:]))


def split_array(array: list[int], part_numer: int) -> list[list[int]]:
    part_numer = min(len(array), part_numer)
    jump = len(array) // part_numer
    split_items = [array[i * jump : (i + 1) * jump] for i in range(part_numer)]
    if len(array) % part_numer != 0:
        split_items[-1] += array[part_numer * jump :]

    return split_items


def connect_arrays(array_1: list[int], array_2: list[int]) -> list[int]:
    pointer_1, pointer_2 = 0, 0
    array = []
    while pointer_1 != len(array_1) and pointer_2 != len(array_2):
        if array_1[pointer_1] <= array_2[pointer_2]:
            array.append(array_1[pointer_1])
            pointer_1 += 1
        else:
            array.append(array_2[pointer_2])
            pointer_2 += 1
    if pointer_1 != len(array_1):
        array += array_1[pointer_1:]
    else:
        array += array_2[pointer_2:]
    return array


def thread_sort_parts(array: list[int], thread_number: int, multiprocess: bool = False) -> list[int]:
    splitted_array = split_array(array, thread_number)
    executor = ProcessPoolExecutor if multiprocess else ThreadPoolExecutor

    with executor(max_workers=thread_number) as executor:
        future_splitted_array = [executor.submit(merge_sort, array_part) for array_part in splitted_array]
        while len(future_splitted_array) > 1:
            array_1 = future_splitted_array.pop().result()
            array_2 = future_splitted_array.pop().result()
            future_splitted_array.append(executor.submit(connect_arrays, array_1, array_2))
        return future_splitted_array[0].result()


def thread_sort_merge(array: list[int], thread_number: int, multiprocess: bool = False) -> list[int]:
    executor_name = ProcessPoolExecutor if multiprocess else ThreadPoolExecutor

    def merge_sort_executor(array: list[int], thread_number: int) -> list[int]:
        if thread_number < 2:
            return merge_sort(array)
        left_array = array[: len(array) // 2]
        right_array = array[len(array) // 2 :]
        left_sorted_array = executor.submit(merge_sort_executor, left_array, thread_number // 2)
        right_sorted_array = executor.submit(merge_sort_executor, right_array, thread_number // 2)
        return connect_arrays(left_sorted_array.result(), right_sorted_array.result())

    with executor_name(max_workers=thread_number) as executor:
        return merge_sort_executor(array, thread_number)
