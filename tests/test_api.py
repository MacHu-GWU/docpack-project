# -*- coding: utf-8 -*-

from docpack import api


def test():
    _ = api


if __name__ == "__main__":
    from docpack.tests import run_cov_test

    run_cov_test(__file__, "docpack.api", preview=False)
