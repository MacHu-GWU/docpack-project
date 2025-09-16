.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.4 (2025-09-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Introduces ``GitHubFileFieldEnum`` and ``ConfluencePageFieldEnum`` enums to allow selective field export in XML serialization for both GitHub and Confluence pipelines. Adds ``wanted_fields`` parameter to pipelines and export methods, enabling users to specify which fields to include in the output. Updates related tests and manual scripts to utilize the new functionality.


0.1.3 (2025-05-28)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- ``ConfluencePipeline.space_id`` now accept both space id or space key.

**Miscellaneous**

- Upgrade pyatlassian dependencies to ``>=0.3.2``.


0.1.2 (2025-04-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Use `pathpick <https://github.com/MacHu-GWU/pathpick-project>`_ to replace the old ``find_matching_files`` implementation.

**Miscellaneous**

- Improve document.
- Migrate to `cookiecutter-pywf_open_source <https://github.com/MacHu-GWU/cookiecutter-pywf_open_source>`_ 0.1.1 code structure.


0.1.1 (2025-03-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Add the following public APIs:
    - ``docpack.api.find_matching_files``
    - ``docpack.api.GitHubFile``
    - ``docpack.api.GitHubPipeline``
    - ``docpack.api.ConfluencePage``
    - ``docpack.api.ConfluencePipeline``
