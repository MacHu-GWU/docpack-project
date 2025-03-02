# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import itertools
import shutil
from datetime import datetime
from functools import cached_property
from pathlib import Path

from osmpoc.paths import dir_project_root, dir_package, dir_unit_test
from osmpoc.docpack import pack_them


dir_repo = dir_project_root.parent.parent


def get_github_url(
    path: Path,
    dir_repo: Path = dir_repo,
    domain: str = "https://github.com",
    org: str = "collegeboard-software",
    repo: str = "msss-searchstream-spikes",
    branch: str = "development",
) -> str:
    """
    Get GitHub URL.

    :param path: /path/to/msss-searchstream-spikes/opensearch/osmpoc-project/README.rst
    :param dir_repo: /path/to/msss-searchstream-spikes
    :param domain: https://github.com
    :param org: collegeboard-software
    :param repo: msss-searchstream-spikes
    :param branch: development

    :return: https://github.com/collegeboard-software/msss-searchstream-spikes/blob/development/opensearch/osmpoc-project/README.rst
    """
    if domain.endswith("/"):
        domain = domain[:-1]
    relpath = path.relative_to(dir_repo)
    return "/".join([domain, org, repo, "blob", branch] + list(relpath.parts))


@dataclasses.dataclass
class GitHubFile:
    path: Path

    @property
    def github_url(self) -> str:
        return get_github_url(path=self.path)

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def relpath(self) -> str:
        return str(self.path.relative_to(dir_repo.parent))

    def to_xml_tag(self) -> str:
        lines = list()
        tab = " " * 2
        lines.append("<document>")
        lines.append(f"{tab}<filename>{self.filename}</filename>")
        lines.append(f"{tab}<path>{self.relpath}</path>")
        lines.append(f"{tab}<github_url>{self.github_url}</github_url>")
        lines.append(f"{tab}<content>")
        lines.append(self.path.read_text())
        lines.append(f"{tab}</content>")
        lines.append("</document>")
        return "\n".join(lines)


@dataclasses.dataclass
class DocSource:
    path: Path
    title: str
    github_url: str

    def get_new_content(self) -> str:
        _lines = self.path.read_text().splitlines()
        lines = [f".."]


def get_metadata_for_doc_folder(path_index: Path) -> DocSource:
    """
    https://github.com/collegeboard-software/msss-searchstream-spikes/blob/development/opensearch/osmpoc-project/docs/source/0170-Sagemaker-Jupyter-Notebook/04-OpenSearch-Index-Alias.ipynb
    :return:
    """
    lines = path_index.read_text().splitlines()
    i = None
    for i, line in enumerate(lines):
        if line == ("=" * len(line)):
            break
    if i is None:
        raise ValueError
    title = lines[i - 1].strip()
    relpath = path_index.relative_to(dir_project_root)
    base_url = "https://github.com/collegeboard-software/msss-searchstream-spikes/blob/development/opensearch/osmpoc-project/"
    github_url = base_url + "/".join(relpath.parts)
    doc = DocSource(
        path=path_index,
        title=title,
        github_url=github_url,
    )
    return doc


# def build_doc_source_for_llm() -> list[DocSource]:
#     doc_list = get_doc_source_list()
#     for doc in doc_list:
#         path_new = dir_tmp.joinpath(f"{doc.title}.rst")
#         lines

if __name__ == "__main__":
    dir_here = Path(__file__).absolute().parent
    dir_tmp = dir_here / "tmp"
    shutil.rmtree(dir_tmp, ignore_errors=True)
    dir_tmp.mkdir(exist_ok=True)
    dt_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    path_out = dir_tmp / f"knowledge_base-{dt_str}.txt"

    # build_doc_source_for_llm()
    local_path_list = [
        dir_here.joinpath("01-OpenSearch-Migration-AI-SME-Instruction.md"),
    ]
    source_path_list = list(dir_package.glob("**/*.py"))
    source_path_list.sort()
    test_path_list = list(dir_unit_test.glob("**/*.py"))
    test_path_list.sort()
    cdk_path_list = list(dir_project_root.joinpath("cdk").glob("**/*.py"))
    cdk_path_list.sort()
    scripts_path_list = list(dir_project_root.joinpath("scripts").glob("**/*.py"))
    scripts_path_list.sort()
    dir_docs_source = dir_project_root / "docs" / "source"
    doc_path_list = [
        path
        for path in dir_docs_source.glob("**/index.rst")
        if path.parts[-2] != "source"
    ]
    doc_path_list.sort()

    path_list = itertools.chain(
        local_path_list,
        source_path_list,
        test_path_list,
        cdk_path_list,
        scripts_path_list,
        doc_path_list,
    )
    github_file_list = [GitHubFile(path=path) for path in path_list]
    lines = list()
    for github_file in github_file_list:
        lines.append(github_file.to_xml_tag())
    content = "\n".join(lines)
    path_out.write_text(content)
