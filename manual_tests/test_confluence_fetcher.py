# -*- coding: utf-8 -*-

from pyatlassian.tests.api_keys import esc_conf
from docpack.confluence_fetcher import (
    load_or_build_page_hierarchy,
    find_matching_pages,
)

space_id = 65697  # business development

sorted_pages = load_or_build_page_hierarchy(
    confluence=esc_conf,
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
    # rprint(page)
    print(page.breadcrumb_path)
