# -*- coding: utf-8 -*-

"""
"""

import typing as T
import json
import shutil
import fnmatch
import dataclasses
from pathlib import Path
from jinja2 import Template


dir_here = Path(__file__).absolute().parent
path_source_code_tpl = dir_here / "source_code_knowledge_base.jinja"
path_test_cases_tpl = dir_here / "test_cases_knowledge_base.jinja"


@dataclasses.dataclass
class PyModule:
    relpath: str = dataclasses.field()
    content: str = dataclasses.field()


def extract_pymodule_list(
    dir_src: Path,
    glob: str = "**/*",
    ignore: T.Optional[T.List[str]] = None,
) -> T.List[PyModule]:
    if ignore is None:
        ignore = []

    pymodule_list = list()

    dirname = dir_src.name
    for path in dir_src.glob(glob):
        relpath = path.relative_to(dir_src)

        # identify whether it should be ignored
        match_ignore = False
        for pattern in ignore:
            match_ignore = fnmatch.fnmatch(str(relpath), pattern)
            if match_ignore is True:
                break

        if match_ignore is True:
            continue

        pymodule = PyModule(
            relpath=str(Path(dirname).joinpath(relpath)),
            content=path.read_text(),
        )
        pymodule_list.append(pymodule)

    # sort by file path
    pymodule_list = list(sorted(pymodule_list, key=lambda x: x.relpath))
    return pymodule_list


def reset_dir_out(dir_out: Path):
    if dir_out.exists():
        shutil.rmtree(dir_out)
    dir_out.mkdir(exist_ok=True)


def generate_source_code_knowledge_base(
    project_name: str,
    dir_src: Path,
    dir_out: Path,
    glob: str = "**/*",
    ignore: T.Optional[T.List[str]] = None,
):
    pymodule_list = extract_pymodule_list(
        dir_src=dir_src,
        glob=glob,
        ignore=ignore,
    )
    tpl = Template(path_source_code_tpl.read_text())
    path_source_code_knowledge_base = dir_out / "source_code_knowledge_base.py"
    content = tpl.render(
        project_name=project_name,
        pymodule_list=pymodule_list,
    )
    path_source_code_knowledge_base.write_text(content)


def generate_test_cases_knowledge_base(
    project_name: str,
    dir_src: Path,
    dir_out: Path,
    glob: str = "**/*",
    ignore: T.Optional[T.List[str]] = None,
):
    pymodule_list = extract_pymodule_list(
        dir_src=dir_src,
        glob=glob,
        ignore=ignore,
    )
    tpl = Template(path_test_cases_tpl.read_text())
    path_test_cases_knowledge_base = dir_out / "test_cases_knowledge_base.py"
    content = tpl.render(
        project_name=project_name,
        pymodule_list=pymodule_list,
    )
    path_test_cases_knowledge_base.write_text(content)


def generate_document_knowledge_base():
    path_readme = dir_project_root / "README.rst"
    path_readme_dst = dir_out / path_readme.name
    path_readme_dst.write_text(path_readme.read_text())

    dir_doc_source = dir_project_root / "docs" / "source"
    for path in dir_doc_source.glob("**/*.rst"):
        relpath = path.relative_to(dir_doc_source)
        parts = list(relpath.parts)
        if len(parts) == 1 or parts[0] in ("_static", package_name):
            continue
        parts.pop()
        name = f"____".join(parts) + ".rst"
        path_out = dir_out / name
        path_out.write_text(path.read_text())


def copy_unit_test_data_reference():
    path_in = dir_project_root.joinpath(
        "scripts",
        "download_unit_test_data",
        "tmp",
        "Atlassian Document Format Parser Unit Test Data.json",
    )
    if path_in.exists():
        path_out = dir_out.joinpath(path_in.name)
        path_out.write_text(path_in.read_text())


dir_out = dir_here / "tmp"
reset_dir_out(dir_out)
dir_project_root = dir_here.parent
package_name = "docpack"  # <=== Change this to your package name

# generate_source_code_knowledge_base
dir_src = dir_project_root / package_name
generate_source_code_knowledge_base(
    project_name=package_name,
    dir_src=dir_src,
    dir_out=dir_out,
    glob="**/*.py",
    ignore=[
        "test/",
        "vendor/*",
    ],
)

# generate_source_code_knowledge_base
dir_src = dir_project_root / "manual_tests"
generate_test_cases_knowledge_base(
    project_name=package_name,
    dir_src=dir_src,
    dir_out=dir_out,
    glob="**/*.py",
    ignore=[],
)

generate_document_knowledge_base()
