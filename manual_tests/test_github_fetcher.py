# -*- coding: utf-8 -*-

"""
Ad-hoc test for the github_fetcher.py module.
"""

from rich import print as rprint
from docpack.paths import dir_project_root, PACKAGE_NAME
from docpack.github_fetcher import (
    find_matching_github_files_from_cloned_folder,
)

github_file_list = find_matching_github_files_from_cloned_folder(
    domain="github.com",
    account="MacHu-GWU",
    repo="dockpack-project",
    branch="main",
    dir_repo=dir_project_root,
    include=[
        f"{PACKAGE_NAME}/**/*.py",
        f"tests/**/*.py",
        f"docs/source/**/index.rst",
    ],
    exclude=[
        f"{PACKAGE_NAME}/tests/**",
        f"{PACKAGE_NAME}/tests/**/*.*",
        f"{PACKAGE_NAME}/vendor/**",
        f"{PACKAGE_NAME}/vendor/**/*.*",
        f"tests/all.py",
        f"tests/**/all.py",
        f"docs/source/index.rst",
    ],
)

for github_file in github_file_list:
    rprint(github_file)
    # print(github_file.path, github_file.github_url)
