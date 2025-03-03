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
    path = Path.home().joinpath(".atlassian", "easyscalecloud", "sanhe-dev.json")
    data = json.loads(path.read_text("utf-8"))
    confluence = pyatlassian.confluence.Confluence(
        url=data["url"],
        username=data["username"],
        password=data["password"],
    )
