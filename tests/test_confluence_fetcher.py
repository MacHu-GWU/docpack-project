# -*- coding: utf-8 -*-

from docpack.confluence_fetcher import (
    extract_id,
    process_include_exclude,
)


def test_extract_id():
    cases = [
        (
            "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/131084/EasyScaleCloud+Value+Proposition",
            "131084",
        ),
        (
            "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/131084/EasyScaleCloud+Value+Proposition/*",
            "131084",
        ),
        (
            "https://easyscalecloud.atlassian.net/wiki/spaces/123/pages/131084/EasyScaleCloud+Value+Proposition",
            "131084",
        ),
        (
            "https://easyscalecloud.atlassian.net/wiki/spaces/123/pages/131084/EasyScaleCloud+Value+Proposition/*",
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
                "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/111111/TitleA",
                "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/222222/TitleA/*",
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


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(__file__, "docpack.confluence_fetcher", preview=False)
