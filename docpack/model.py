# -*- coding: utf-8 -*-

import typing as T
from pydantic import BaseModel, Field

from .constants import TAB


class Document(BaseModel):
    uri: str = Field()
    title: str = Field()
    description: str = Field()
    content: str = Field()

    def to_xml(self) -> str:
        lines = list()

        lines.append("<document>")
        lines.append(f"{TAB}<uri>{self.uri}</filename>")
        lines.append(f"{TAB}<title>{self.title}</path>")
        lines.append(f"{TAB}<description>")
        lines.append(self.description)
        lines.append(f"{TAB}</description>")
        lines.append(f"{TAB}<content>")
        lines.append(self.path.read_text())
        lines.append(f"{TAB}</content>")
        lines.append("</document>")

        return "\n".join(lines)


# class GitHubRepo(BaseModel):
#     domain: str = dataclasses.field()
#     account: str = dataclasses.field()
#     repo: str = dataclasses.field()
#     branch: str = dataclasses.field()
