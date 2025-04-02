
.. image:: https://readthedocs.org/projects/docpack/badge/?version=latest
    :target: https://docpack.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/docpack-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/docpack-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/docpack-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/docpack-project

.. image:: https://img.shields.io/pypi/v/docpack.svg
    :target: https://pypi.python.org/pypi/docpack

.. image:: https://img.shields.io/pypi/l/docpack.svg
    :target: https://pypi.python.org/pypi/docpack

.. image:: https://img.shields.io/pypi/pyversions/docpack.svg
    :target: https://pypi.python.org/pypi/docpack

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/docpack-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/docpack-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://docpack.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://docpack.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/docpack-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/docpack-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/docpack-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/docpack#files


Welcome to ``docpack`` Documentation
==============================================================================
.. image:: https://docpack.readthedocs.io/en/latest/_static/docpack-logo.png
    :target: https://docpack.readthedocs.io/en/latest/

DocPack is a Python utility library designed to efficiently consolidate documentation from multiple sources (GitHub, Confluence, and local file systems) into a single, AI-accessible knowledge base. It provides tools for retrieving, formatting, and packaging document content with consistent structure to facilitate efficient reference by Large Language Models.

For example, this `generate_knowledge_base.py <https://github.com/MacHu-GWU/docpack-project/blob/main/genai/generate_knowledge_base.py>`_ script converts the `docpack <https://github.com/MacHu-GWU/docpack-project>`_ GitHub repository into an `all_in_one_knowledge_base.txt <https://github.com/MacHu-GWU/docpack-project/blob/main/genai/sample_knowledge_base/all_in_one_knowledge_base.txt>`_ file. It is concatenated from all of the files in the `sample_knowledge_base <https://github.com/MacHu-GWU/docpack-project/tree/main/genai/sample_knowledge_base>`_ directory.


.. _install:

Install
------------------------------------------------------------------------------

``docpack`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install docpack

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade docpack
