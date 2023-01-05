#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021-2023 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""GEO Knowledge Hub Package Loader."""

from geo_package_loader.api import GEOKnowledgeHubApi
from geo_package_loader.service import PackageLoaderService
from geo_package_loader.store import TokenStore


class PackageLoader:
    """Package Loader class.

    This class enable users to interact with the GEO Knowledge Hub services
    to upload and publish complete Knowledge Packages.
    """

    def __init__(self, access_token: str, package_api: str, record_api: str):
        """Initializer.

        Args:
            access_token (str): Access token of the GEO Knowledge Hub.

            package_api (str): Address to the Package API.

            record_api (str): Address to the Record API.
        """
        # Configuring the token store
        TokenStore.save_token(access_token)

        # Defining API
        self._api = GEOKnowledgeHubApi(package_api, record_api)

    @property
    def service(self):
        """Package Loader service accessor."""
        return PackageLoaderService(self._api)
