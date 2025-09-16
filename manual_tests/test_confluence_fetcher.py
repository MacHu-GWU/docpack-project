# -*- coding: utf-8 -*-

"""
Ad-hoc test for the confluence_fetcher.py module.
"""

from docpack.confluence_fetcher import (
    load_or_build_page_hierarchy,
    find_matching_pages,
)
from docpack.tests.confluence import confluence
from rich import print as rprint

space_id = 65697  # business development

sorted_pages = load_or_build_page_hierarchy(
    confluence=confluence,
    space_id=space_id,
    cache_key="2025-03-02",
)
matched_pages = find_matching_pages(
    sorted_pages=sorted_pages,
    include=[
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/3178507/Products/*",
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/46792705/Services/*",
    ],
    exclude=[
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/3113056/ESC+Data+Pipeline+for+DynamoDB+-+Competitive+Analysis/*",
        "https://easyscalecloud.atlassian.net/wiki/spaces/BD/pages/56197124/Service+Catalog",
    ],
)

# for page in sorted_pages:
for page in matched_pages:
    rprint(page)
    # print(page.breadcrumb_path)
