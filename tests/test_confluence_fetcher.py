# -*- coding: utf-8 -*-

import uuid
import shutil

from docpack.cache import cache
from docpack.tests.confluence import confluence
from docpack.confluence_fetcher import (
    extract_id,
    process_include_exclude,
    ConfluencePipeline,
)
from docpack.paths import (
    dir_project_root,
    dir_tmp,
    PACKAGE_NAME,
)


def test_extract_id():
    cases = [
        (
            "https://example.atlassian.net/wiki/spaces/BD/pages/131084/Value+Proposition",
            "131084",
        ),
        (
            "https://example.atlassian.net/wiki/spaces/BD/pages/131084/Value+Proposition/*",
            "131084",
        ),
        (
            "https://example.atlassian.net/wiki/spaces/123/pages/131084/Value+Proposition",
            "131084",
        ),
        (
            "https://example.atlassian.net/wiki/spaces/123/pages/131084/Value+Proposition/*",
            "131084",
        ),
        ("131084", "131084"),
        ("131084/*", "131084"),
    ]
    for url, expected_id in cases:
        assert extract_id(url) == expected_id


def test_process_include_exclude():
    cases = [
        (
            [],
            [],
            [],
            [],
        ),
        (
            [
                "https://example.atlassian.net/wiki/spaces/BD/pages/111111/TitleA",
                "https://example.atlassian.net/wiki/spaces/BD/pages/222222/TitleA/*",
                "333333",
                "444444/*",
            ],
            [],
            [
                "111111",
                "222222/*",
                "333333",
                "444444/*",
            ],
            [],
        ),
    ]
    for include, exclude, expected_include, expected_exclude in cases:
        new_include, new_exclude = process_include_exclude(include, exclude)
        assert new_include == expected_include
        assert new_exclude == expected_exclude


class TestConfluencePipeline:
    def test_fetch(self):
        space_id = 68321325 # docpack Unit Test
        cache_key = str(uuid.uuid4())
        shutil.rmtree(dir_tmp, ignore_errors=True)

        confluence_pipeline = ConfluencePipeline(
            confluence=confluence,
            space_id=space_id,
            cache_key=cache_key,
            include=[
                f"{confluence.url}/wiki/spaces/DOCPACKUT/pages/70647810/Topic+1/*",
                f"{confluence.url}/wiki/spaces/DOCPACKUT/pages/70647820/Topic+2/*",
            ],
            exclude=[
                f"{confluence.url}/wiki/spaces/DOCPACKUT/pages/71008257/topic+1+-+design/*",
                f"{confluence.url}/wiki/spaces/DOCPACKUT/pages/70713375/topic+2+-+document+2",
            ],
            dir_out=dir_tmp,
        )
        confluence_pipeline.fetch()


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(
        __file__,
        "docpack.confluence_fetcher",
        preview=False,
    )
