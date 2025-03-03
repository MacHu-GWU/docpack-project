# -*- coding: utf-8 -*-

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
        space_id = 65697
        cache_key = "2025-03-01"  # business development
        shutil.rmtree(dir_tmp, ignore_errors=True)
        real_cache_key = (confluence.url, space_id, cache_key)
        cache.delete(real_cache_key)

        confluence_pipeline = ConfluencePipeline(
            confluence=confluence,
            space_id=space_id,
            cache_key=cache_key,
            include=[
                f"{confluence.url}/wiki/spaces/BD/pages/3178507/Products/*",
                f"{confluence.url}/wiki/spaces/BD/pages/46792705/Services/*",
            ],
            exclude=[
                f"{confluence.url}/wiki/spaces/BD/pages/3113056/Data+Pipeline+for+DynamoDB+-+Competitive+Analysis/*",
                f"{confluence.url}/wiki/spaces/BD/pages/56197124/Service+Catalog",
            ],
            dir_out=dir_tmp,
        )
        confluence_pipeline.fetch()


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(__file__, "docpack.confluence_fetcher", preview=False)
