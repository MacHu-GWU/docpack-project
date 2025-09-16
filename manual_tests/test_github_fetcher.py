# -*- coding: utf-8 -*-

"""
Ad-hoc test for the github_fetcher.py module.
"""

from docpack.github_fetcher import (
    find_matching_github_files_from_cloned_folder,
    GitHubPipeline,
)
from docpack.paths import dir_project_root, PACKAGE_NAME


dir_repo = dir_project_root
# dir_repo = Path.home().joinpath("Downloads", "docpack-project-main")

domain = "https://github.com"
account = "MacHu-GWU"
repo = "docpack-project"
branch = "main"
include = [
    f"{PACKAGE_NAME}/**/*.py",
    f"tests/**/*.py",
    f"docs/source/**/index.rst",
]
exclude = [
    f"{PACKAGE_NAME}/tests/**",
    f"{PACKAGE_NAME}/tests/**/*.*",
    f"{PACKAGE_NAME}/vendor/**",
    f"{PACKAGE_NAME}/vendor/**/*.*",
    f"tests/all.py",
    f"tests/**/all.py",
    f"docs/source/index.rst",
]

github_file_list = find_matching_github_files_from_cloned_folder(
    domain=domain,
    account=account,
    repo=repo,
    branch=branch,
    dir_repo=dir_repo,
    include=include,
    exclude=exclude,
)

for github_file in github_file_list:
    #     rprint(github_file)
    print(github_file.path, github_file.github_url)
