# -*- coding: utf-8 -*-

from docpack import api


def test():
    _ = api
    _ = api.cache
    _ = api.find_matching_files
    _ = api.GitHubFile
    _ = api.GitHubPipeline
    _ = api.ConfluencePage
    _ = api.ConfluencePipeline


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(__file__, "docpack.api", preview=False)
