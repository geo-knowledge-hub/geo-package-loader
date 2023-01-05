..
    This file is part of GEO Knowledge Hub Package Loader.
    Copyright (C) 2021 GEO Secretariat.

    GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


================================
GEO Knowledge Hub Package Loader
================================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/geo-knowledge-hub/geo-package-loader/blob/master/LICENSE
        :alt: Software License


.. image:: https://readthedocs.org/projects/geo_package_loader/badge/?version=latest
        :target: https://geo_package_loader.readthedocs.io/en/latest/
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-maturing-blue.svg
        :target: https://www.tidyverse.org/lifecycle/#maturing
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/geo-knowledge-hub/geo-package-loader.svg
        :target: https://github.com/geo-knowledge-hub/geo-package-loader/releases
        :alt: Release


.. image:: https://img.shields.io/discord/730739436551143514?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/730739436551143514#
        :alt: Join us at Discord


About
-----

Load Knowledge Packages metadata and related resources to the GEO Knowledge Hub digital library.

Install
-------

**1.** Install from the GitHub repository::

    pip3 install git+https://github.com/geo-knowledge-hub/geo-package-loader.git


Install (Development mode)
--------------------------

**1.** Use ``git`` to clone the software repository::

    git clone https://github.com/geo-knowledge-hub/geo-package-loader.git


**2.** Go to the source code folder::

    cd geo-package-loader


**3.** Install in development mode::

    pip3 install -e .[tests,docs]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.8::

        python3.8 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip wheel setuptools


Usage
-----

The Package Loader installs a command line tool named ``geo-package-loader``. The example below shows how to use it to upload a ``Knowledge Package``::

    geo-package-loader load --verbose \
                            --packages-api https://<YOUR-API-ADDRESS>/api/packages \
                            --records-api  https://<YOUR-API-ADDRESS>/api/records \
                            --access-token <YOUR-ACCESS-TOKEN> \
                            --knowledge-package-repository <DIRECTORY-WHERE-PACKAGE-IS-DEFINED>


Knowledge Package Repository
----------------------------

To use the ``geo-package-loader``,  you must have defined a ``Knowledge Package Repository``, a directory containing the elements you will use to build the package, its resources, and data files.

A ``Knowledge Package Repository`` must contain the file ``knowledge-package.json`` at its root. This file specifies which and how the files in the directory are to be used. An example of the file format is presented below:

.. code-block:: json

        {
            "knowledge_package": {
                "metadata_file": "package/metadata.json",
                "files": [
                    "package/data.txt"
                ],
                "options": {
                    "include_doi": true
                }
        },
        "resources":  [
                {
                    "metadata_file": "resources/resource-01.json",
                    "files": [
                        "resources/data.txt"
                    ],
                    "options": {
                        "include_doi": false
                    }
                },
                {
                    "metadata_file": "resources/resource-02.json"
                }
            ]
        }


As you can see, the file is separated into two sections:

- ``knowledge_package``: In this section, you define where the file with the metadata for the ``Knowledge Package`` that is to be published is located, along with the files that are to be uploaded;

- ``resources``: List with the definition of the ``Knowledge Resources``` that must be created and associated with the package. The internal definition structure for each resource is the same as for the package.

From the code block, in addition to defining metadata (`metadata_file`) and files (`files`), it is possible to define extra options. The available option, `include_doi`, specifies that the tool should request the GEO Knowledge Hub to reserve DOIs for resources.

Also, you should note that if a specific definition, such as `files` or `extra options`, is not required, they do not need to be defined in the ``knowledge-package.json`` file.

License
-------


.. admonition::
    Copyright 2021-2023 GEO Secretariat.

    GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
