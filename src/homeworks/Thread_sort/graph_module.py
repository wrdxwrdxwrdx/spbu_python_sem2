import argparse
import random
import time
from typing import Callable

import matplotlib.pyplot as plt

from src.homeworks.Thread_sort.sorting_module import *


def check_time_ms(
    sorting_function: Callable[[list[int], int], list[int]] | Callable[[list[int]], list[int]],
    size: int,
    n_tries: int = 5,
    *args: int,
    **kwargs: bool,
) -> float:
    start = time.perf_counter()
    for _ in range(n_tries):
        array = [random.randint(-100, 100) for _ in range(size)]
        sorting_function(array, *args, **kwargs)
    return (time.perf_counter() - start) * 1000 / n_tries


def create_graph(
    size: int,
    threads: list[int],
    output_path: str,
    multiprocess: bool = False,
    second_function: bool = False,
    n_tries: int = 5,
) -> None:
    if second_function:
        thread_y = [
            check_time_ms(thread_sort_merge, size, n_tries, thread_number, multiprocess=multiprocess)
            for thread_number in threads
        ]
    else:
        thread_y = [
            check_time_ms(thread_sort_parts, size, n_tries, thread_number, multiprocess=multiprocess)
            for thread_number in threads
        ]

    plt.title(f"size: {size}")
    plt.plot(threads, thread_y, label="multiprocess sort" if multiprocess else "thread sort")
    merge_y = [check_time_ms(merge_sort, size, n_tries) for _ in threads]
    plt.plot(threads, merge_y, label="merge sort")

    plt.xlabel("number of processes" if multiprocess else "number of threads")
    plt.ylabel("time(ms)")
    plt.legend()

    plt.savefig(output_path)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--size", type=int, default=100000, help="array size for test")
    argparser.add_argument(
        "--threads", type=int, default=[1, 2, 3, 4, 5, 6, 7, 8], help="a set of threads used for tests", nargs="+"
    )
    argparser.add_argument(
        "--output_path",
        type=str,
        default="graph.png",
        help="the path to the file where the graph with the results will be saved",
    )
    argparser.add_argument(
        "--multiprocess", action="store_true", help="is it necessary to create threads in different processes"
    )

    argparser.add_argument("--second_function", action="store_true", help="use second thread function")

    args = argparser.parse_args()

    try:
        create_graph(**vars(args))
    except Exception as error:
        print(error)
