# -*- coding: utf-8 -*-

"""
GitHub file extraction and synchronization utilities for documentation packaging.

This module provides tools for retrieving, processing, and exporting files from GitHub
repositories, with a focus on preparing content for AI knowledge bases and documentation
systems. It includes capabilities for file filtering with glob patterns, metadata
enrichment, XML serialization, and structured export. The module's core components are
the :class:`GitHubFile` class, which represents individual repository files with their content
and metadata, and the :class:`GitHubPipeline` class, which orchestrates the entire process of
extracting files matching specific criteria and exporting them to a target location.
The resulting exported files preserve both content and contextual information, making
them suitable for knowledge extraction, documentation generation, and AI context building.
"""

import typing as T
import hashlib
from pathlib import Path

from pydantic import BaseModel, Field

from .constants import TAB, GitHubFileFieldEnum
from .find_matching_files import find_matching_files


def extract_domain(url: str) -> str:
    """
    Extract the domain part from a URL.

    This function takes a URL as input and returns just the domain name,
    removing any protocol prefixes (http://, https://) and any paths or
    parameters that might follow the domain.

    :param url: A URL string (e.g., "https://github.com/abc-team/xyz-project")
    :return: The domain part of the URL (e.g., "github.com")

    Examples:
        >>> extract_domain("https://github.com/abc-team/xyz-project")
        'github.com'
        >>> extract_domain("http://github.com")
        'github.com'
    """
    # Remove protocol part (http:// or https://)
    if "://" in url:
        domain = url.split("://")[1]
    else:
        domain = url

    # Remove any paths or parameters after the domain
    domain = domain.split("/")[0]

    return domain


def get_github_url(
    domain: str,
    account: str,
    repo: str,
    branch: str,
    path_parts: tuple[str, ...],
) -> str:
    """
    Generate a GitHub URL for a file in a repository.
    """
    path = "/".join(path_parts)
    return f"https://{domain}/{account}/{repo}/blob/{branch}/{path}"


class GitHubFile(BaseModel):
    """
    A data container representing a file in a GitHub repository with metadata and content.

    This class provides utilities for working with GitHub files, including methods for
    serializing to LLM friendly XML format, generating unique identifiers based on
    the file path, and exporting the file data to disk.

    :param domain: The domain name of the GitHub instance (e.g., 'github.com')
    :param account: The GitHub account or organization name
    :param repo: The name of the GitHub repository
    :param branch: The branch name (e.g., 'main', 'master') or tag name.
    :param github_url: The full URL to the file on GitHub, this is usually
        a calculated value.
    :param path_parts: The file path broken into components
    :param title: An optional title for the file
    :param description: An optional description of the file
    :param content: The raw content of the file
    """

    domain: str = Field()
    account: str = Field()
    repo: str = Field()
    branch: str = Field()
    github_url: str = Field()
    path_parts: tuple[str, ...] = Field()
    title: str = Field()
    description: str = Field()
    content: str = Field()

    @property
    def path(self) -> str:
        """
        Get the relative path of the file from the repository root.

        :returns: The path as a string with components joined by '/'
        """
        return "/".join(self.path_parts)

    def to_xml(
        self,
        wanted_fields: list[str] | None = None,
    ) -> str:
        """
        Serialize the file data to XML format.

        This method generates an XML representation of the file including its GitHub
        metadata and content, suitable for document storage or AI context input.
        """
        if wanted_fields is None:
            wanted_fields = [field.value for field in GitHubFileFieldEnum]
        lines = list()

        lines.append("<document>")
        if GitHubFileFieldEnum.source_type.value in wanted_fields:
            field = GitHubFileFieldEnum.source_type.value
            lines.append(f"{TAB}<{field}>GitHub Repository</{field}>")
        if GitHubFileFieldEnum.github_url.value in wanted_fields:
            field = GitHubFileFieldEnum.github_url.value
            lines.append(f"{TAB}<{field}>{self.github_url}</{field}>")
        if GitHubFileFieldEnum.account.value in wanted_fields:
            field = GitHubFileFieldEnum.account.value
            lines.append(f"{TAB}<{field}>{self.account}</{field}>")
        if GitHubFileFieldEnum.repo.value in wanted_fields:
            field = GitHubFileFieldEnum.repo.value
            lines.append(f"{TAB}<{field}>{self.repo}</{field}>")
        if GitHubFileFieldEnum.branch.value in wanted_fields:
            field = GitHubFileFieldEnum.branch.value
            lines.append(f"{TAB}<{field}>{self.branch}</{field}>")
        if GitHubFileFieldEnum.path.value in wanted_fields:
            field = GitHubFileFieldEnum.path.value
            lines.append(f"{TAB}<{field}>{self.path}</{field}>")
        if self.title:
            if GitHubFileFieldEnum.title.value in wanted_fields:
                field = GitHubFileFieldEnum.title.value
                lines.append(f"{TAB}<{field}>{self.title}</{field}>")
        if self.description:
            if GitHubFileFieldEnum.description.value in wanted_fields:
                field = GitHubFileFieldEnum.description.value
                lines.append(f"{TAB}<{field}>")
                lines.append(self.description)
                lines.append(f"{TAB}</{field}>")
        if GitHubFileFieldEnum.content.value in wanted_fields:
            field = GitHubFileFieldEnum.content.value
            lines.append(f"{TAB}<{field}>")
            lines.append(self.content)
            lines.append(f"{TAB}</{field}>")
        lines.append("</document>")
        return "\n".join(lines)

    @property
    def uri_hash(self) -> str:
        """
        Generate a short hash identifier for the file.

        Creates a unique identifier based on the file's GitHub location including
        domain, account, repo, branch, and path. This hash can be used for
        creating unique filenames or identifiers.

        :returns: A 7-character hash string derived from the file's URI
        """
        hash_key = f"{self.domain}/{self.account}/{self.repo}/{self.branch}/{self.path}"
        return hashlib.sha256(hash_key.encode("utf-8")).hexdigest()[:7]

    @property
    def breadcrumb_path(self) -> str:
        """
        Create a flattened representation of the file path.

        Converts the hierarchical path structure into a single string with
        path components joined by '~' characters. This format is useful for
        creating filesystem-safe filenames that preserve path information.

        :returns: The path with components joined by '~' instead of '/'
        """
        return "~".join(self.path_parts)

    def export_to_file(
        self,
        dir_out: Path,
        wanted_fields: list[str] | None = None,
    ) -> Path:
        """
        Export the file data as an XML document to the specified directory.

        Creates an XML file in the specified directory with a filename that
        combines the breadcrumb path and URI hash to ensure uniqueness.

        :param dir_out: The directory where the XML file should be saved

        :returns: The path to the created XML file
        """
        path_out = dir_out.joinpath(f"{self.breadcrumb_path}~{self.uri_hash}.xml")
        content = self.to_xml(wanted_fields=wanted_fields)
        try:
            path_out.write_text(content, encoding="utf-8")
        except FileNotFoundError as e:
            path_out.parent.mkdir(parents=True)
            path_out.write_text(content, encoding="utf-8")
        return path_out


def sort_github_files(
    github_file_list: list[GitHubFile],
) -> list[GitHubFile]:
    """
    Sort GitHub files by their relative path within the repository.

    This function takes a list of :class:`GitHubFile` objects and returns a new list
    sorted alphabetically by their path property. Sorting helps maintain
    consistent ordering when processing or displaying files.

    :param github_file_list: A list of :class:`GitHubFile` objects to sort

    :returns: A new list containing the same :class:`GitHubFile` objects
        but sorted by their paths
    """
    return list(sorted(github_file_list, key=lambda x: x.path))


def find_matching_github_files_from_cloned_folder(
    domain: str,
    account: str,
    repo: str,
    branch: str,
    dir_repo: Path,
    include: list[str],
    exclude: list[str],
) -> list[GitHubFile]:
    """
    Find and process files from a local clone of a GitHub repository.

    This function scans a local directory containing a Git repository clone,
    matches files based on include/exclude patterns, and converts matching
    files into GitHubFile objects with appropriate metadata. The function uses
    the find_matching_files utility to apply pattern filtering.

    :param domain: The domain of the GitHub instance (e.g., 'github.com')
    :param account: The GitHub account or organization name
    :param repo: The name of the GitHub repository
    :param branch: The branch name (e.g., 'main', 'master') or tag name.
    :param dir_repo: Path to the root of the cloned repository
    :param include: List of glob patterns specifying which files to include
            (e.g., ["*.py", "docs/**/*.md"])
    :param exclude: List of glob patterns specifying which files to exclude
            (e.g., ["**/__pycache__/**", "**/.git/**"])

    :returns: A sorted list of :class:`GitHubFile` objects representing the
        matching files from the repository

    .. note::

        This function uses
        `get_web_url <https://github.com/MacHu-GWU/git_web_url-project>`_
        from git_web_url.api to generate the GitHub URL for each file based on
        its local path.
    """
    domain = extract_domain(domain)
    github_file_list = list()
    for path in find_matching_files(
        dir_root=dir_repo,
        include=include,
        exclude=exclude,
    ):
        path_parts = path.relative_to(dir_repo).parts
        github_url = get_github_url(
            domain=domain,
            account=account,
            repo=repo,
            branch=branch,
            path_parts=path_parts,
        )
        github_file = GitHubFile(
            domain=domain,
            account=account,
            repo=repo,
            branch=branch,
            github_url=github_url,
            path_parts=path_parts,
            title="",
            description="",
            content=path.read_text(encoding="utf-8"),
        )
        github_file_list.append(github_file)

    return sort_github_files(github_file_list)


class GitHubPipeline(BaseModel):
    """
    A data pipeline that extracts and synchronizes files from a GitHub repository to a target location.

    GitHubPipeline provides an abstraction for defining a GitHub repository source and
    a set of file filters, then synchronizing the matching files to a specified output directory.
    This pipeline handles the entire workflow from selecting files to saving them as structured
    XML documents that preserve both content and metadata.

    :param domain: The domain of the GitHub instance (e.g., 'github.com')
    :param account: The GitHub account or organization name
    :param repo: The name of the GitHub repository
    :param branch: The branch name (e.g., 'main', 'master') or tag name.
    :param dir_repo: Path to the root of the cloned repository
    :param include: List of glob patterns specifying which files to include
            (e.g., ["*.py", "docs/**/*.md"])
    :param exclude: List of glob patterns specifying which files to exclude
            (e.g., ["**/__pycache__/**", "**/.git/**"])
    :param dir_out: The directory where the XML files should be exported.
    """

    domain: str = Field()
    account: str = Field()
    repo: str = Field()
    branch: str = Field()
    dir_repo: Path = Field()
    include: list[str] = Field()
    exclude: list[str] = Field()
    dir_out: Path = Field()
    wanted_fields: list[str] | None = Field(default=None)

    def model_post_init(self, __context: T.Any) -> None:
        self.domain = extract_domain(self.domain)

    def post_process_github_file(self, github_file: GitHubFile) -> GitHubFile:
        return github_file

    def post_process_path_out(self, github_file: GitHubFile, path_out: Path):
        pass

    def fetch(self):
        """
        Execute the pipeline to extract and export GitHub files to the target directory.

        This method performs the complete workflow:

        1. Finds all files in the local repository that match the include/exclude patterns
        2. Converts each file to a GitHubFile object with metadata
        3. Exports each file as an XML document to the specified output directory
        """
        github_file_list = find_matching_github_files_from_cloned_folder(
            domain=self.domain,
            account=self.account,
            repo=self.repo,
            branch=self.branch,
            dir_repo=self.dir_repo,
            include=self.include,
            exclude=self.exclude,
        )
        for github_file in github_file_list:
            github_file = self.post_process_github_file(github_file)
            path_out = github_file.export_to_file(
                dir_out=self.dir_out,
                wanted_fields=self.wanted_fields,
            )
            self.post_process_path_out(github_file=github_file, path_out=path_out)
