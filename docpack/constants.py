# -*- coding: utf-8 -*-

"""
Constants and Enums for DocPack
"""

import enum

TAB = " " * 2


class GitHubFileFieldEnum(str, enum.Enum):
    """
    Enum for GitHub file fields.
    """

    source_type = "source_type"
    github_url = "github_url"
    account = "account"
    repo = "repo"
    branch = "branch"
    path = "path"
    title = "title"
    description = "description"
    content = "content"


class ConfluencePageFieldEnum(str, enum.Enum):
    """
    Enum for Confluence page fields.
    """

    source_type = "source_type"
    confluence_url = "confluence_url"
    title = "title"
    markdown_content = "markdown_content"
