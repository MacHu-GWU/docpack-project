# -*- coding: utf-8 -*-

"""
Confluence page fetching and processing utilities.
"""

import typing as T
import json
import gzip
from pathlib import Path
from functools import cached_property

from diskcache import Cache
from pydantic import BaseModel, Field, ConfigDict
import pyatlassian.api as pyatlassian
import atlas_doc_parser.api as atlas_doc_parser

from .constants import TAB, ConfluencePageFieldEnum
from .paths import dir_cache


class ConfluencePage(BaseModel):
    """
    A data container for Confluence pages that enriches the API response data with
    hierarchical metadata and navigation properties.

    This class wraps the raw page data returned by Confluence's
    `get pages <https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-get>`_ API
    and adds additional attributes for working with page hierarchies and navigation.

    :param page_data: The raw item response from the `Confluence.get_pages` API call
    :param site_url: Base URL of the Confluence site
    :param id_path: Hierarchical ID-based path (e.g., "/parent_id/child_id")
        for filtering with glob patterns
    :param position_path: Position-based path (e.g., "/1/3/2") used for hierarchical sorting
    :param breadcrumb_path: Human-readable title hierarchy (e.g., "|| Parent || Child || Page")
        similar to UI breadcrumbs

    The class assumes the body format is
    `Atlas Doc Format <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_

    Properties like `id`, `title`, `parent_id` provide convenient access to commonly
    used attributes from the raw page data.
    """

    page_data: dict[str, T.Any] = Field()
    site_url: str = Field()
    id_path: T.Optional[str] = Field()
    position_path: T.Optional[str] = Field()
    breadcrumb_path: T.Optional[str] = Field()

    @property
    def space_id(self) -> str:
        return self.page_data["spaceId"]

    @property
    def id(self) -> str:
        return self.page_data["id"]

    @property
    def parent_id(self) -> str:
        return self.page_data["parentId"]

    @property
    def parent_type(self) -> str:
        return self.page_data["parentType"]

    @property
    def title(self) -> str:
        return self.page_data["title"]

    @property
    def position(self) -> int:
        return self.page_data["position"]

    @property
    def atlas_doc(self) -> dict[str, T.Any]:
        return json.loads(self.page_data["body"]["atlas_doc_format"]["value"])

    @property
    def webui_url(self) -> str:
        webui_link = self.page_data["_links"]["webui"]
        webui_url = f"{self.site_url}/wiki{webui_link}"
        return webui_url

    @property
    def markdown(self) -> str:
        node_doc = atlas_doc_parser.NodeDoc.from_dict(
            dct=self.atlas_doc,
            ignore_error=True,
        )
        md_content = node_doc.to_markdown(ignore_error=True)
        lines = [
            f"# {self.title}",
            "",
        ]
        lines.extend(md_content.splitlines())
        md_content = "\n".join(lines)
        return md_content

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
            wanted_fields = [field.value for field in ConfluencePageFieldEnum]
        lines = list()
        lines.append("<document>")
        if ConfluencePageFieldEnum.source_type.value in wanted_fields:
            field = ConfluencePageFieldEnum.source_type.value
            lines.append(f"{TAB}<{field}>Confluence Page</{field}>")
        if ConfluencePageFieldEnum.confluence_url.value in wanted_fields:
            field = ConfluencePageFieldEnum.confluence_url.value
            lines.append(f"{TAB}<{field}>{self.webui_url}</{field}>")
        if ConfluencePageFieldEnum.title.value in wanted_fields:
            field = ConfluencePageFieldEnum.title.value
            lines.append(f"{TAB}<{field}>{self.title}</{field}>")
        # if self.description:
        #     lines.append(f"{TAB}<description>")
        #     lines.append(self.description)
        #     lines.append(f"{TAB}</description>")
        if ConfluencePageFieldEnum.markdown_content.value in wanted_fields:
            field = ConfluencePageFieldEnum.markdown_content.value
            lines.append(f"{TAB}<{field}>")
            lines.append(self.markdown)
            lines.append(f"{TAB}</{field}>")
        lines.append("</document>")

        return "\n".join(lines)

    def export_to_file(
        self,
        dir_out: Path,
        wanted_fields: list[str] | None = None,
    ) -> Path:
        fname = self.breadcrumb_path[3:].replace("||", "~")
        basename = f"{fname}.xml"
        path_out = dir_out.joinpath(basename)
        content = self.to_xml(wanted_fields=wanted_fields)
        try:
            path_out.write_text(content, encoding="utf-8")
        except FileNotFoundError:
            path_out.parent.mkdir(parents=True)
            path_out.write_text(content, encoding="utf-8")
        return path_out


def fetch_raw_pages_from_space(
    confluence: pyatlassian.confluence.Confluence,
    space_id: int,
) -> list[ConfluencePage]:
    """
    Crawls and retrieves all pages from a Confluence space using pagination.

    This function fetches raw page data from the Confluence API, converts each page
    to a ConfluencePage object with minimal initialization, and returns the complete
    collection without processing hierarchical relationships.

    :param confluence: Authenticated Confluence API client
    :param space_id: ID of the Confluence space to crawl

    :returns: List of :class:`ConfluencePage` objects with initialized page_data and site_url,
        but without hierarchy information (id_path, position_path, breadcrumb_path)
    """
    paginator = confluence.pagi_get_pages(
        space_id=[int(space_id)],
        body_format="atlas_doc_format",
    )
    confluence_page_list = list()
    for ith, response in enumerate(paginator, start=1):
        for page_data in response.get("results", []):
            confluence_page = ConfluencePage(
                page_data=page_data,
                site_url=confluence.url,
                id_path=None,
                position_path=None,
                breadcrumb_path=None,
            )
            confluence_page_list.append(confluence_page)
    return confluence_page_list


def enrich_pages_with_hierarchy_data(
    raw_pages: list[ConfluencePage],
) -> list[ConfluencePage]:
    """
    Enriches Confluence page objects with hierarchical relationship information.

    This function processes a list of raw ConfluencePage objects to:

    1. Create ID-based paths (id_path) representing the page hierarchy
    2. Generate position-based paths (position_path) for correct sorting
    3. Build human-readable title hierarchies (breadcrumb_path) for display

    The function creates a complete hierarchy tree by iteratively processing pages
    for up to 20 levels of depth, starting with parent pages and moving to children.

    :param raw_pages: List of :class:`ConfluencePage` objects with basic data but no hierarchy info

    :returns: List of :class:`ConfluencePage` objects enriched with hierarchy data and sorted by
        their position in the hierarchy
    """
    # Create a mapping of page IDs to page objects for quick lookups
    id_to_page_mapping: dict[str, ConfluencePage] = {
        page.id: page for page in raw_pages
    }

    # Create a working copy of the mapping to track unprocessed pages
    remaining_pages = dict(id_to_page_mapping)

    # Limit recursion depth to avoid infinite loops with circular references
    max_next_level = 20

    # Process pages level by level, starting from root pages
    for ith in range(1, 1 + max_next_level):
        # print(
        #     f"=== {ith = }, {len(remaining_pages) = }, {len(id_to_page_mapping) = }"
        # )
        # Exit if all pages have been processed
        if len(remaining_pages) == 0:
            break

        # Process each remaining page
        for id, page in list(remaining_pages.items()):
            # Process root pages (no parent or parent outside our space)
            if page.parent_id is None:
                # Create hierarchy paths for root pages
                path = f"/{page.id}"
                sort_key = f"/{page.position}"
                title_chain = f"|| {page.title}"
                page.id_path = path
                page.position_path = sort_key
                page.breadcrumb_path = title_chain
                # Remove from remaining pages as it's now processed
                remaining_pages.pop(page.id)

            # Process child pages
            else:
                # Check if the parent page is in our collection
                if page.parent_id in id_to_page_mapping:
                    parent_page = id_to_page_mapping[page.parent_id]
                    # Skip if parent's paths aren't set yet (will process in later iteration)
                    if parent_page.id_path is None:
                        continue

                    # Create hierarchy paths based on parent's paths
                    page.id_path = f"{parent_page.id_path}/{id}"
                    page.position_path = f"{parent_page.position_path}/{page.position}"
                    page.breadcrumb_path = (
                        f"{parent_page.breadcrumb_path} || {page.title}"
                    )

                    # Remove from remaining pages as it's now processed
                    remaining_pages.pop(id)

                # Handle pages with parents outside our scope (typically Confluence folders)
                else:
                    # Remove these pages from both mappings as they can't be processed
                    remaining_pages.pop(id)
                    id_to_page_mapping.pop(id)

    # Sort pages based on their positions in the hierarchy
    sorted_pages = list(
        sorted(
            id_to_page_mapping.values(),
            key=lambda page: page.position_path,
        )
    )

    return sorted_pages


def load_or_build_page_hierarchy(
    confluence: pyatlassian.confluence.Confluence,
    space_id: int,
    cache: Cache,
    cache_key: str,
    expire: int = 24 * 60 * 60,
) -> list[ConfluencePage]:
    """
    Retrieves a complete Confluence page hierarchy with caching support.

    This function either:

    1. Returns a cached page hierarchy if available
    2. Or fetches pages, builds their hierarchy, and caches the result

    The function uses a composite cache key consisting of the Confluence URL,
    space ID, and provided cache key to ensure proper cache isolation.
    Results are compressed with gzip before caching to reduce storage usage.

    :param confluence: Authenticated Confluence API client
    :param space_id: ID of the Confluence space to crawl
    :param cache_key: Additional key component for cache differentiation
        (e.g., to cache different point-in-time snapshot of the same space)

    :returns: List of :class:`ConfluencePage` objects with complete hierarchy data,
        sorted by their hierarchical position
    """
    real_cache_key = (confluence.url, space_id, cache_key)
    # print(f"{real_cache_key = }")  # for debug only
    if real_cache_key in cache:  # pragma: no cover
        print("Hit cache!")  # for debug only
        cache_value = cache[real_cache_key]
        data = json.loads(gzip.decompress(cache_value).decode("utf-8"))
        sorted_pages = [ConfluencePage(**page_data) for page_data in data]
        return sorted_pages
    else:
        raw_pages = fetch_raw_pages_from_space(
            confluence=confluence,
            space_id=space_id,
        )
        sorted_pages = enrich_pages_with_hierarchy_data(raw_pages=raw_pages)
        data = [page.model_dump() for page in sorted_pages]
        cache_value = gzip.compress(
            json.dumps(data, ensure_ascii=False).encode("utf-8")
        )
        cache.set(real_cache_key, cache_value, expire=expire)
        return sorted_pages


def extract_id(url_or_id: str) -> str:
    """
    Extract the page ID from a Confluence URL or return the ID if directly provided.

    This function handles different Confluence URL formats and extracts the page ID.
    It also handles cases where the URL has a trailing /* or when just the ID is provided.

    :param url_or_id: A Confluence page URL or direct page ID.
        Example: "https://example.atlassian.net/wiki/spaces/BD/pages/123456/Value+Proposition"
        or just "123456"

    :return: The extracted page ID as a string
    """
    # If it's just an ID (possibly with /* at the end)
    if "/" not in url_or_id or url_or_id.count("/") == 1 and url_or_id.endswith("/*"):
        # Remove /* if present
        return url_or_id.rstrip("/*")

    # It's a URL, extract the ID which comes after /pages/ segment
    parts = url_or_id.split("/pages/")
    if len(parts) != 2:
        raise ValueError(f"Invalid Confluence URL format: {url_or_id}")

    # The ID is the segment after /pages/ and before the next /
    id_and_title = parts[1].split("/", 1)
    return id_and_title[0]


def process_include_exclude(
    include: list[str],
    exclude: list[str],
) -> tuple[list[str], list[str]]:
    """
    Process include and exclude patterns for Confluence page IDs or URLs.

    This function takes lists of include and exclude patterns that might be
    Confluence page URLs or IDs, extracts the page IDs from them, and preserves
    any trailing wildcards (/*). It normalizes all inputs to a consistent format
    of either just the ID or ID with wildcard.

    :param include: List of Confluence page URLs or IDs to include
        Items can be full URLs, page IDs, or patterns with /* suffix
    :param exclude: List of Confluence page URLs or IDs to exclude
        Items can be full URLs, page IDs, or patterns with /* suffix

    :return: A tuple of two lists:
        1. Normalized include patterns with extracted IDs
        2. Normalized exclude patterns with extracted IDs
    """
    new_include, new_exclude = list(), list()
    for expr in include:
        id = extract_id(expr)
        if expr.endswith("/*"):
            new_include.append(id + "/*")
        else:
            new_include.append(id)
    for expr in exclude:
        id = extract_id(expr)
        if expr.endswith("/*"):
            new_exclude.append(id + "/*")
        else:
            new_exclude.append(id)
    return new_include, new_exclude


def is_matching(
    page_mapping: dict[str, ConfluencePage],
    page: ConfluencePage,
    include: T.List[str],
    exclude: T.List[str],
) -> bool:
    """
    Determine if a Confluence page matches the include/exclude filtering criteria.

    This function implements the filtering logic similar to gitignore patterns, where:

    - A page is included if it matches any include pattern
    - A page is excluded if it matches any exclude pattern
    - Patterns with /* suffix match the specified page and all its descendants
    - If no include patterns are provided, all pages are initially included (before exclusions)

    :param page_mapping: Dictionary mapping page IDs to their ConfluencePage objects
        for efficient parent-child relationship lookups
    :param page: The ConfluencePage object to check against the filters
    :param include: List of normalized page IDs or page ID patterns (with /* suffix)
        to include in results. This is a processed "include" list from process_include_exclude()
    :param exclude: List of normalized page IDs or page ID patterns (with /* suffix)
        to exclude from results. This is a processed "exclude" list from process_include_exclude()

    :return: True if the page should be included in the results, False otherwise
    """
    # Process include patterns - a page must match at least one include pattern to be considered
    if len(include):
        include_flag = False
        for expr in include:
            if expr.endswith("/*"):
                # This is a hierarchical include pattern (folder and all children)
                parent_id = expr.rstrip("/*")
                if parent_id in page_mapping:
                    parent_page = page_mapping[parent_id]
                    # Check if current page is a descendant of the specified parent
                    if page.id_path.startswith(parent_page.id_path):
                        include_flag = True
                        break
            elif page.id == expr.rstrip("/*"):
                # Direct page ID match
                include_flag = True
                break
    else:
        # No include patterns specified - include all pages by default
        include_flag = True

    # If page didn't match any include patterns, exclude it
    if include_flag is False:
        return False

    # Process exclude patterns - a page matching any exclude pattern is filtered out
    for expr in exclude:
        if expr.endswith("/*"):
            # This is a hierarchical exclude pattern (folder and all children)
            parent_id = expr.rstrip("/*")
            if parent_id in page_mapping:
                parent_page = page_mapping[parent_id]
                # Check if current page is a descendant of the excluded parent
                if page.id_path.startswith(parent_page.id_path):
                    return False
        elif page.id == expr.rstrip("/*"):
            # Direct page ID match for exclusion
            return False

    # Page didn't hit all exclude filter criteria
    return True


def find_matching_pages(
    sorted_pages: list[ConfluencePage],
    include: T.List[str],
    exclude: T.List[str],
):
    """
    Filter Confluence pages based on include/exclude patterns similar to gitignore.

    This function lets you specify which pages to include or exclude using either
    direct page IDs or hierarchical patterns. It supports URL or ID formats and
    allows using /* suffix to indicate a page and all its descendants (like a folder).

    Filtering logic follows these rules:

    1. First, normalize all URL or ID patterns to a consistent format
    2. Pages matching any include pattern are considered (or all if no include patterns)
    3. Then, any page matching an exclude pattern is filtered out
    4. Patterns with /* match the specified page and all its descendants

    :param sorted_pages: List of :class:`ConfluencePage` objects sorted by hierarchy
        (typically from `enrich_pages_with_hierarchy_data`)
    :param include: List of Confluence page URLs or IDs to include
        Can be full URLs, page IDs, or patterns with /* suffix
    :param exclude: List of Confluence page URLs or IDs to exclude
        Can be full URLs, page IDs, or patterns with /* suffix

    :return: Filtered list of :class:`ConfluencePage` objects that match the criteria
    """
    page_mapping = {page.id: page for page in sorted_pages}
    matched_pages = list()
    new_include, new_exclude = process_include_exclude(include, exclude)
    for page in sorted_pages:
        flag = is_matching(
            page_mapping=page_mapping,
            page=page,
            include=new_include,
            exclude=new_exclude,
        )
        if flag:
            matched_pages.append(page)
    return matched_pages


class ConfluencePipeline(BaseModel):
    """
    A data pipeline that extracts and synchronizes Confluence pages to a target location.

    ConfluencePipeline provides an abstraction for defining a Confluence space source and
    filtering criteria, then exporting the matching pages to a specified output directory
    as structured XML documents that preserve both content and metadata.

    The pipeline handles the complete workflow from authentication to content extraction,
    hierarchical processing, filtering, and file export with metadata preservation.

    Example:

    .. code-block:: python

        confluence_pipeline = ConfluencePipeline(
            confluence=confluence,
            space_id=space_id,
            # Use cache key to avoid re-fetching the same page hierarchy
            # it will store all pages in the cache and use it for filtering
            # if you change the include / exclude pattern
            cache_key=cache_key,
            include=[
                # include all child page
                f"{confluence.url}/wiki/spaces/{space_key}/pages/{page_id}/{page_title}/*",
                # only include this page, no child page
                f"{confluence.url}/wiki/spaces/{space_key}/pages/{page_id}/{page_title}",
            ],
            exclude=[
                # exclude all child page
                f"{confluence.url}/wiki/spaces/{space_key}/pages/{page_id}/{page_title}/*",
                # only exclude this page, no child page
                f"{confluence.url}/wiki/spaces/{space_key}/pages/{page_id}/{page_title}",
            ],
        )


    :param confluence: Authenticated Confluence API client instance
    :param space_id: space ID (int) or space key (str) of the Confluence space to process
    :param include: List of patterns (URLs or IDs) specifying which pages to include.
        Use Page URL + ``/*`` to include all children of a page.
    :param exclude: List of patterns (URLs or IDs) specifying which pages to exclude
        Use Page URL + ``/*`` to include all children of a page.
    :param dir_out: The directory where the XML files should be exported
    :param cache_key: Key for caching and retrieving page hierarchies
    :param cache_expire: Cache expiration time in seconds (default: 24 hours)
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    confluence: "pyatlassian.confluence.Confluence" = Field()
    space_id: int | str = Field()
    include: list[str] = Field()
    exclude: list[str] = Field()
    dir_out: Path = Field()
    cache_key: str = Field()
    cache_expire: int = Field(default=24 * 60 * 60)
    cache_path: str = Field(default=str(dir_cache))
    wanted_fields: list[str] | None = Field(default=None)

    @cached_property
    def _space_id(self) -> int:
        """
        Get the space ID from the provided space_id.
        """
        if isinstance(self.space_id, str):
            res = self.confluence.get_spaces(
                keys=[self.space_id],
            )
            space_id = None
            for dct in res.get("results", []):
                if dct.get("key") == self.space_id:
                    space_id = int(dct["id"])
                    return space_id
            if space_id is None:  # pragma: no cover
                raise ValueError("Space not found")
        else:
            return self.space_id

    @cached_property
    def cache(self) -> Cache:
        return Cache(self.cache_path)

    def post_process_confluence_page(
        self,
        confluence_page: ConfluencePage,
    ) -> ConfluencePage:
        """
        Post-process the ConfluencePage object after fetching it.

        User can override this method to add custom processing logic
        """
        return confluence_page

    def post_process_path_out(
        self,
        confluence_page: ConfluencePage,
        path_out: Path,
    ):
        """
        Post-process the output path after exporting a Confluence page.
        """
        pass

    def fetch(self):
        """
        Execute the pipeline to extract and export Confluence pages to the target directory.

        This method performs the complete workflow:

        1. List all pages in the given Confluence space that match the include/exclude patterns
        2. Converts each page to a ConfluencePage object with metadata
        3. Exports each page as an XML document to the specified output directory
        """
        sorted_pages = load_or_build_page_hierarchy(
            confluence=self.confluence,
            space_id=self._space_id,
            cache_key=self.cache_key,
            cache=self.cache,
        )
        matched_pages = find_matching_pages(
            sorted_pages=sorted_pages,
            include=self.include,
            exclude=self.exclude,
        )
        for page in matched_pages:
            page = self.post_process_confluence_page(page)
            path_out = page.export_to_file(
                dir_out=self.dir_out, wanted_fields=self.wanted_fields
            )
            self.post_process_path_out(confluence_page=page, path_out=path_out)
