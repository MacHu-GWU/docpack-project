# -*- coding: utf-8 -*-

import shutil
from docpack.github_fetcher import (
    extract_domain,
    GitHubPipeline,
)
from docpack.paths import (
    dir_project_root,
    dir_tmp,
    PACKAGE_NAME,
)


def test_extract_domain():
    cases = [
        (
            "https://github.com/abc-team/xyz-project",
            "github.com",
        ),
        (
            "https://github.com/",
            "github.com",
        ),
        (
            "https://github.com",
            "github.com",
        ),
        (
            "http://github.com/",
            "github.com",
        ),
        (
            "http://github.com",
            "github.com",
        ),
    ]
    for url, expected_domain in cases:
        assert extract_domain(url) == expected_domain


class TestGitHubPipeline:
    def test_fetch(self):
        shutil.rmtree(dir_tmp, ignore_errors=True)
        gh_pipeline = GitHubPipeline(
            domain="https://github.com",
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
            dir_out=dir_tmp,
        )
        assert gh_pipeline.domain == "github.com"
        gh_pipeline.fetch()


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(__file__, "docpack.github_fetcher", preview=False)
