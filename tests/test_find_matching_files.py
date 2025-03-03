# -*- coding: utf-8 -*-

from docpack.paths import dir_project_root
from docpack.find_matching_files import (
    remove_dupes,
    process_include_exclude,
    find_matching_files,
)


def _test_remove_dupes(in_list: list, out_list: list):
    assert remove_dupes(in_list) == out_list
    assert id(in_list) != id(out_list)


def test_remove_dupes():
    cases = [
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, 2, 3, 1, 4], [1, 2, 3, 4]),
        ([1, 1, 1, 1], [1]),
        (["a", "b", "a", "c", "b", "d"], ["a", "b", "c", "d"]),
        (["1", "2", "1", "3"], ["1", "2", "3"]),
        (list(range(1000)) + list(range(500)), list(range(1000))),
    ]
    for in_list, out_list in cases:
        _test_remove_dupes(in_list, out_list)


def _test_process_include_exclude(
    include: list[str],
    exclude: list[str],
    expected_include: list[str],
    expected_exclude: list[str],
):
    result_include, result_exclude = process_include_exclude(include, exclude)
    assert result_include == expected_include
    assert result_exclude == expected_exclude


def test_process_include_exclude():
    cases = [
        # Test default behavior with empty lists
        ([], [], ["**/*.*"], []),
        # Test with only include patterns
        (["*.py", "*.txt"], [], ["*.py", "*.txt"], []),
        # Test with only exclude patterns
        (
            [],
            ["*.pyc", "__pycache__/**"],
            ["**/*.*"],
            ["*.pyc", "__pycache__/**"],
        ),
        # Test with both include and exclude patterns
        (
            ["*.py", "*.txt"],
            ["test_*.py", "temp.txt"],
            ["*.py", "*.txt"],
            ["test_*.py", "temp.txt"],
        ),
        # Test deduplication of include patterns
        (
            ["*.py", "*.py", "*.txt", "*.txt"],
            [],
            ["*.py", "*.txt"],
            [],
        ),
        # Test deduplication of exclude patterns
        (
            [],
            ["*.pyc", "*.pyc", "__pycache__/**", "__pycache__/**"],
            ["**/*.*"],
            ["*.pyc", "__pycache__/**"],
        ),
        # Test deduplication of both patterns
        (
            ["*.py", "*.py", "*.txt"],
            ["test_*.py", "test_*.py", "temp.txt"],
            ["*.py", "*.txt"],
            ["test_*.py", "temp.txt"],
        ),
        (
            ["src/**/*.py", "tests/**/*.py"],
            ["**/__pycache__/**", "**/*.pyc"],
            ["src/**/*.py", "tests/**/*.py"],
            ["**/__pycache__/**", "**/*.pyc"],
        ),
        (
            ["*.PY", "*.py"],
            ["*.Pyc", "*.pYc"],
            ["*.PY", "*.py"],
            ["*.Pyc", "*.pYc"],
        ),
        (
            ["test-*.py", "test_?.txt"],
            ["*[0-9].py", "*-temp.*"],
            ["test-*.py", "test_?.txt"],
            ["*[0-9].py", "*-temp.*"],
        ),
    ]
    for include, exclude, expected_include, expected_exclude in cases:
        _test_process_include_exclude(
            include,
            exclude,
            expected_include,
            expected_exclude,
        )


def test_find_matching_files_case_1():
    res = find_matching_files(
        dir_root=dir_project_root,
        include=["docpack/**/*.py", "docs/source/**/*.rst"],
        exclude=[],
    )
    for path in res:
        print(path)


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(__file__, "docpack.find_matching_files", preview=False)
