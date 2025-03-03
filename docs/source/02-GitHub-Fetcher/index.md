# GitHub Document Fetching Tutorial

This tutorial demonstrates how to use the [docpack](https://github.com/MacHu-GWU/docpack-project) library to efficiently extract and process documentation from GitHub repositories. Whether you're building an AI knowledge base, centralizing documentation across multiple projects, or preparing content for analysis, ``docpack`` provides a streamlined way to fetch, transform, and organize GitHub files with rich metadata. By following this notebook, you'll learn how to set up document extraction pipelines that can filter files using glob patterns, preserve contextual information like repository structure, and output consistently formatted files ready for integration with AI systems or documentation platforms. This approach eliminates manual document gathering and ensures your knowledge base stays synchronized with your source repositories.

## Setting Up the GitHub Fetching Pipeline

Before diving into the actual implementation, let's understand how to use the ``GitHubPipeline`` class to extract documents from GitHub repositories. This approach allows you to selectively fetch files while preserving their original context and metadata.
The code below demonstrates setting up a pipeline that fetches selected files from a GitHub repository. The pipeline uses glob patterns to determine which files to include and exclude - a powerful pattern-matching approach similar to ``.gitignore`` files.


```python
import shutil
from pathlib import Path

from docpack.github_fetcher import GitHubPipeline
```


```python
dir_here = Path.cwd().absolute()
dir_tmp = dir_here / "tmp"
print(f"{dir_tmp = !s}")
shutil.rmtree(dir_tmp, ignore_errors=True)

dir_repo = Path.cwd().parent.parent.parent
print(f"{dir_repo = !s}")
```

    dir_tmp = /Users/sanhehu/Documents/GitHub/docpack-project/docs/source/02-GitHub-Fetcher/tmp
    dir_repo = /Users/sanhehu/Documents/GitHub/docpack-project


**Key Points About File Filtering**

Include-Exclude Pattern Matching:

1. The pipeline uses glob patterns to filter files
    - If a file matches ANY pattern in the include list, it's initially considered for inclusion
    - If a file matches ANY pattern in the exclude list, it's excluded regardless of inclusion rules
    - If both include and exclude patterns match a file, exclusion takes precedence
2. Understanding Glob Patterns:
    - Patterns are relative to the repository root
    - ``**/*.py`` means "any Python file in any directory or subdirectory"
    - ``/**/`` indicates recursive matching through all subdirectories
    - For expression in ``exclude``, it is not exactly the glob pattern. For example ``exclude = ["docpack/tests/**", ...]`` means exclude any file in ``docpack/tests`` directory but not in subdirectories, in order to exclude all files in ``docpack/tests`` directory and subdirectories, you have to do both.
    - Simple patterns like ``README.rst`` match specific files
3. ``dir_out`` specifies the directory where the AI friendly XML files should be exported.

When the ``fetch()`` method is called, the pipeline processes all files matching the include patterns (but not matching exclude patterns) and exports them to the specified output directory with their metadata intact.


```python
gh_pipeline = GitHubPipeline(
    domain="github.com",
    account="MacHu-GWU",
    repo="docpack-project",
    branch="main",
    dir_repo=dir_repo,
    include=[
        f"README.rst",
        "docpack/**/*.py",
        "tests/**/*.py",
        "docs/source/**/index.rst",
    ],
    exclude=[
        "docpack/tests/**",
        "docpack/tests/**/*.*",
        "docpack/vendor/**",
        "docpack/vendor/**/*.*",
        "tests/all.py",
        "tests/**/all.py",
        "docs/source/index.rst",
    ],
    dir_out=dir_tmp,
)
gh_pipeline.fetch()
```

## Exploring the Extracted Documents

After running the pipeline, let's examine the output files to understand what docpack produces. The code below displays the first 500 characters from five randomly selected output files:


```python
for path in list(dir_tmp.glob("*.xml"))[:5]:
    print("#" + "=" * 60)
    print(f"| content of {path.name!r}")
    print("#" + "=" * 60)
    print(path.read_text()[:500] + "\n...")
```

    #============================================================
    | content of 'docpack~paths.py~e12af5d.xml'
    #============================================================
    <document>
      <source_type>GitHub Repository</source_type>
      <github_url>https://github.com/MacHu-GWU/docpack-project/blob/main/docpack/paths.py</github_url>
      <account>MacHu-GWU</account>
      <repo>docpack-project</repo>
      <branch>main</branch>
      <path>docpack/paths.py</path>
      <content>
    # -*- coding: utf-8 -*-
    
    from pathlib import Path
    
    dir_here = Path(__file__).absolute().parent
    dir_package = dir_here
    PACKAGE_NAME = dir_here.name
    dir_home = Path.home()
    
    dir_project_root = dir_here.parent
    dir_tmp
    ...
    #============================================================
    | content of 'tests~test_api.py~9fb2de7.xml'
    #============================================================
    <document>
      <source_type>GitHub Repository</source_type>
      <github_url>https://github.com/MacHu-GWU/docpack-project/blob/main/tests/test_api.py</github_url>
      <account>MacHu-GWU</account>
      <repo>docpack-project</repo>
      <branch>main</branch>
      <path>tests/test_api.py</path>
      <content>
    # -*- coding: utf-8 -*-
    
    from docpack import api
    
    
    def test():
        _ = api
    
    
    if __name__ == "__main__":
        from docpack.tests import run_cov_test
    
        run_cov_test(__file__, "docpack.api", preview=False)
    
      </c
    ...
    #============================================================
    | content of 'docpack~__init__.py~98a2489.xml'
    #============================================================
    <document>
      <source_type>GitHub Repository</source_type>
      <github_url>https://github.com/MacHu-GWU/docpack-project/blob/main/docpack/__init__.py</github_url>
      <account>MacHu-GWU</account>
      <repo>docpack-project</repo>
      <branch>main</branch>
      <path>docpack/__init__.py</path>
      <content>
    # -*- coding: utf-8 -*-
    
    """
    DocPack efficiently consolidates documentation from GitHub, Confluence, and files into a structured knowledge base for AI access.
    """
    
    from ._version import __version__
    
    __short_
    ...
    #============================================================
    | content of 'tests~test_github_fetcher.py~b480033.xml'
    #============================================================
    <document>
      <source_type>GitHub Repository</source_type>
      <github_url>https://github.com/MacHu-GWU/docpack-project/blob/main/tests/test_github_fetcher.py</github_url>
      <account>MacHu-GWU</account>
      <repo>docpack-project</repo>
      <branch>main</branch>
      <path>tests/test_github_fetcher.py</path>
      <content>
    # -*- coding: utf-8 -*-
    
    import shutil
    from docpack.github_fetcher import (
        extract_domain,
        GitHubPipeline,
    )
    from docpack.paths import (
        dir_project_root,
        dir_tmp,
        PACK
    ...
    #============================================================
    | content of 'docpack~github_fetcher.py~6458e19.xml'
    #============================================================
    <document>
      <source_type>GitHub Repository</source_type>
      <github_url>https://github.com/MacHu-GWU/docpack-project/blob/main/docpack/github_fetcher.py</github_url>
      <account>MacHu-GWU</account>
      <repo>docpack-project</repo>
      <branch>main</branch>
      <path>docpack/github_fetcher.py</path>
      <content>
    # -*- coding: utf-8 -*-
    
    """
    GitHub file extraction and synchronization utilities for documentation packaging.
    
    This module provides tools for retrieving, processing, and exporting files from Git
    ...


Each extracted file is saved in a structured XML format that preserves both the content and rich contextual metadata from the original GitHub repository. The XML structure includes:

- ``<source_type>``: Identifies the origin as a GitHub repository
- ``<github_url>``: Direct link to view the file in GitHub's web interface
- ``<account>``, ``<repo>``, ``<branch>``: Repository metadata for complete context
- ``<path>``: The file's location within the repository structure
- ``<content>``: The actual file content, preserved exactly as in the original

This format is particularly valuable for AI-powered documentation systems and knowledge bases because it maintains the complete context of each file. When using this data with an AI assistant, the assistant can not only access the file content but also provide source links for verification, understand the file's position in the project hierarchy, and maintain references to the original repository.

Notice how the filenames contain both the path (with '~' replacing '/') and a unique hash, ensuring each file has a distinct, identifiable name while preserving its original location information.
