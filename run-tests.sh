#!/usr/bin/env bash
#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

pydocstyle gkh_package_loader setup.py && \
isort gkh_package_loader setup.py --check-only --diff #&& \
#check-manifest --ignore ".travis.yml,.drone.yml,.readthedocs.yml" #&& \
#sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest && \
#pytest
