# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

from pyatlassian.tests.api_keys import esc_conf

from docpack.paths import dir_project_root, PACKAGE_NAME
from docpack.constants import ConfluencePageFieldEnum
from docpack.github_fetcher import GitHubPipeline
from docpack.confluence_fetcher import ConfluencePipeline

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here / "tmp"
shutil.rmtree(dir_tmp, ignore_errors=True)
dir_tmp.mkdir()

gh_pipeline = GitHubPipeline(
    domain="github.com",
    account="MacHu-GWU",
    repo="dockpack-project",
    branch="main",
    dir_repo=dir_project_root,
    include=[
        f"README.rst",
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
gh_pipeline.fetch()

confluence_pipeline = ConfluencePipeline(
    confluence=esc_conf,
    space_id=65697,  # BD, business development
    cache_key="2025-03-02",
    include=[
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/3178507/Products/*",
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/46792705/Services/*",
    ],
    exclude=[
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/3113056/ESC+Data+Pipeline+for+DynamoDB+-+Competitive+Analysis/*",
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/56197124/Service+Catalog",
    ],
    dir_out=dir_tmp,
    wanted_fields=[
        ConfluencePageFieldEnum.source_type,
        ConfluencePageFieldEnum.title,
        ConfluencePageFieldEnum.markdown_content,
    ]
)
confluence_pipeline.fetch()
