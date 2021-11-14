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


**1.** Use ``git`` to clone the software repository::

    git clone https://github.com/geo-knowledge-hub/geo-package-loader.git


**2.** Go to the source code folder::

    cd geo-package-loader


**3.** Install in development mode::

    pip3 install -e .[all]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.8::

        python3.8 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools


Usage
-----


The Package Loader installs a command line tool named ``geo-package-loader``. The example below shows how to use it to upload a Knowledge package::

    geo-package-loader load --verbose \
                            --url https://127.0.0.1:5000/api \
                            --access-token k3pnxWYjM9cYYU5EZXVhiHCWMYKDlTIs5Sp1NRbGIp3NpSCmRP06CgHaGZ5d \
                            --knowledge-package /home/gribeiro/Devel/github/gqueiroz/demo-knowledge-packages/bdc/knowledge-package.json \
                            --resources-dir /home/gribeiro/Devel/github/gqueiroz/demo-knowledge-packages/bdc


Knowledge Package File
----------------------


The ``knowledge-package.json`` file above has the following structure:


.. code-block:: json

    {
        "knowledge_package": {
            "metadata_file": "bdc-lulc.json",
            "resources": [
                "pdf/bdc-lulc-user-guide.pdf",
                "videos/gkhub-bdc-lulc.mp4"
            ]
        },
        "components":  [
            {
                "metadata_file": "dataset-lulc-maps.json",
                "resources": [
                    "pdf/bdc-lulc-maps.pdf",
                    "maps/CB4_64_16D_STK_1.zip",
                    "maps/LC8_30_16D_STK_1.zip"
                ]
            },
            {
                "metadata_file": "dataset-datacube.json",
                "resources": [
                    "pdf/bdc-datacube.pdf"
                ]
            }
        ]
    }


Access Token
------------


In order to create an access token to be used to create records and upload files through InvenioRDM REST API, use the ``invenio tokens create`` command::

    invenio tokens create --name gkhub-ingest --user email@mail.org


This will output a key such as::

    k3pnxWYjM9cYYU5EZXVhiHCWMYKDlTIs5Sp1NRbGIp3NpSCmRP06CgHaGZ5d


If you do not have a base user, perform the following commands::

    invenio users create email@mail.org --password=123456 --active

    invenio roles add email@mail.org admin


License
-------


.. admonition::
    Copyright 2021 GEO Secretariat.

    GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
