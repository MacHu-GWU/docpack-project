# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path

import pyatlassian.api as pyatlassian


if "CI" in os.environ:
    url = os.environ["CONF_URL"]
    username = os.environ["CONF_USERNAME"]
    password = os.environ["CONF_PASSWORD"]
    confluence = pyatlassian.confluence.Confluence(
        url=url,
        username=username,
        password=password,
    )
else:
    from home_secret.api import hs

    url = hs.v("providers.atlassian.accounts.sh.site_url")
    username = hs.v("providers.atlassian.accounts.sh.users.sh.email")
    password = hs.v("providers.atlassian.accounts.sh.users.sh.secrets.sync_page.value")
    confluence = pyatlassian.confluence.Confluence(
        url=url,
        username=username,
        password=password,
    )