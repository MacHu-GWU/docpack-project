# -*- coding: utf-8 -*-

from pathlib import Path

dir_here = Path(__file__).absolute().parent
dir_package = dir_here
PACKAGE_NAME = dir_here.name
dir_home = Path.home()

dir_project_root = dir_here.parent
dir_tmp = dir_project_root / "tmp"

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"

# doc related
dir_docs_source = dir_project_root / "docs" / "source"

# ------------------------------------------------------------------------------
# Application Related
# ------------------------------------------------------------------------------
dir_project_home = dir_home / PACKAGE_NAME
dir_project_home.mkdir(parents=True, exist_ok=True)
dir_cache = dir_project_home / ".cache"
