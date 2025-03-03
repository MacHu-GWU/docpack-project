# -*- coding: utf-8 -*-

"""
Provides utilities for finding files in a directory hierarchy using glob patterns.
This module offers functions to efficiently filter files by include/exclude patterns,
similar to .gitignore functionality. It supports recursive directory traversal,
pattern matching, and duplicate handling, making it ideal for selectively processing
files in complex directory structures while maintaining a clean filtering approach.
"""

import typing as T
import itertools
from pathlib import Path


def remove_dupes(lst: list) -> list:
    """
    Remove duplicates from a list while preserving order.

    This function returns a new list containing unique elements from the input list,
    maintaining their original order. The input list remains unchanged, and the
    returned list has a different identity (i.e., a new object in memory).
    """
    return list(dict.fromkeys(lst))


def process_include_exclude(
    include: list[str],
    exclude: list[str],
) -> tuple[list[str], list[str]]:
    """
    Process include and exclude glob patterns to prepare them for file filtering operations.

    This function normalizes the include and exclude pattern lists by:

    1. Setting a default include pattern of ["**/*.*"] if none provided
    2. Removing duplicate patterns from both lists while preserving order
    """
    if not include:
        include = ["**/*.*"]
    include = remove_dupes(include)
    exclude = remove_dupes(exclude)
    return include, exclude


def find_matching_files(
    dir_root: Path,
    include: list[str],
    exclude: list[str],
) -> T.Iterable[Path]:
    """
    Find files in a directory that match include patterns but not exclude patterns.

    This function recursively searches through the directory tree starting from dir_root,
    filtering files using two sets of glob patterns:

    1. First, files are included if they match any pattern in the include list
       (or all files if include list is empty)
    2. Then, matching files are excluded if they match any pattern in the exclude list

    :param dir_root: The root directory to start the search from
    :param include: List of glob patterns to match files for inclusion
        If empty, defaults to ["**/*.*"] (all files)
    :param exclude: List of glob patterns to exclude files from the results
        If empty, no files are excluded
    """
    # process input parameter
    if not dir_root.exists() or not dir_root.is_dir():
        raise ValueError(f"Directory {dir_root} does not exist or is not a directory")
    include, exclude = process_include_exclude(
        include=include,
        exclude=exclude,
    )
    # print(f"{include = }, {exclude = }")  # for debug only

    # find matching files
    st = set()
    for path in itertools.chain(*[dir_root.glob(expr) for expr in include]):
        # print(f"{path = !s}")
        if path in st:
            continue
        st.add(path)
        relpath = path.relative_to(dir_root)
        should_exclude = any(relpath.match(pattern) for pattern in exclude)
        if should_exclude is False:
            yield path
