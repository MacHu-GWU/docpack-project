# -*- coding: utf-8 -*-

from docpack.paths import dir_project_root, PACKAGE_NAME
from docpack.find_matching_files import find_matching_files

paths = find_matching_files(
    dir_root=dir_project_root,
    include=[
        f"{PACKAGE_NAME}/**/*.py",
        f"tests/**/*.py",
        f"docs/source/**/index.rst",
    ],
    exclude=[
        f"{PACKAGE_NAME}/tests/**",
        f"{PACKAGE_NAME}/tests/**/*.*",
        f"{PACKAGE_NAME}/vendor/**",
        f"{PACKAGE_NAME}/vendor/**/*.*",
        f"tests/all.py",
        f"tests/**/all.py",
        f"docs/source/index.rst",
    ],
)
paths = list(paths)
paths.sort()
for path in paths:
    print(path)
