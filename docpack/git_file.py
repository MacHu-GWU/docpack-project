# -*- coding: utf-8 -*-

"""
Pack multiple document into one to fit AI application.
"""

import typing as T
import dataclasses
from pathlib import Path


class FileData(T.TypedDict):
    filename: str
    path: str
    content: str


@dataclasses.dataclass
class File:
    path: Path = dataclasses.field()
    relpath: T.Optional[Path] = dataclasses.field(default=None)

    def to_xml_data(self) -> dict[str, str]:
        return {
            "filename": self.path.name,
            "path": str(self.path) if self.relpath is None else str(self.relpath),
            "content": self.path.read_text(),
        }


def serialize_to_xml(file_data_list: list[FileData]) -> str:
    lines = []
    for file_data in file_data_list:
        lines.append("<document>")

        lines.append("  <filename>{}</filename>".format(file_data["filename"]))
        lines.append("  <path>{}</path>".format(file_data["path"]))

        lines.append("  <content>")
        lines.append(file_data["content"])
        lines.append("  </content>")
        lines.append("</document>")
    return "\n".join(lines)


def pack_them(
    in_path_list: list[Path],
    out_path: Path,
    root_path: T.Optional[Path] = None,
):
    if root_path is None:
        file_data_list = [File(path=path).to_xml_data() for path in in_path_list]
    else:
        file_data_list = [
            File(path=path, relpath=path.relative_to(root_path)).to_xml_data()
            for path in in_path_list
        ]
    out_path.write_text(serialize_to_xml(file_data_list=file_data_list))
