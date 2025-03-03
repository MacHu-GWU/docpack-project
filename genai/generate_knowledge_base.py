# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

from docpack.paths import dir_project_root, PACKAGE_NAME
from docpack.github_fetcher import GitHubPipeline

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here / "tmp"
shutil.rmtree(dir_tmp, ignore_errors=True)
dir_tmp.mkdir()

gh_pipeline = GitHubPipeline(
    domain="github.com",
    account="MacHu-GWU",
    repo=f"{PACKAGE_NAME}-project",
    branch="main",
    dir_repo=dir_project_root,
    include=[
        "README.rst",
        f"{PACKAGE_NAME}/**/*.py",
        "tests/**/*.py",
        "docs/source/**/index.rst",
        "docs/source/**/index.md",
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
    dir_out=dir_tmp,
)
gh_pipeline.fetch()
