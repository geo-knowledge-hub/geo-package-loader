#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021-2023 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""GEO Knowledge Hub Package Loader service."""

from pydash import py_

from pathlib import Path
from typing import Union, Dict

from geo_package_loader.api import GEOKnowledgeHubApi
from geo_package_loader.repository import load_package_repository


class PackageLoaderService:
    """Package Loader Service.

    This service contains a high-level API to enable users to
    easily import and publish packages and resources to the
    GEO Knowledge Hub.
    """

    def __init__(self, api: GEOKnowledgeHubApi):
        """Initializer.

        Args:
            api (GEOKnowledgeHubApi): API object to interact with the GEO Knowledge Hub service.
        """
        self._api = api

    #
    # Base methods
    #
    def _load_element(self, element_definition, type_):
        """Load an element to the GEO Knowledge Hub service."""
        include_doi = py_.get(element_definition, "options.include_doi", False)

        # create draft
        element_definition["metadata"] = self._api.create_draft(
            element_definition["metadata"], type_
        )

        # upload files
        element_definition["metadata"] = self._api.upload_files(
            element_definition["metadata"], element_definition["files"], type_
        )

        # include DOI
        if include_doi:
            element_definition["metadata"] = self._api.reserve_doi(
                element_definition["metadata"]
            )

        return element_definition

    #
    # High-Level methods.
    #
    def load_package(
        self, package_repository: Union[str, Path], publish: bool = True
    ) -> Dict:
        """Load a package and its resources to the GEO Knowledge Hub.

        Args:
            package_repository (Union[str, Path]): Directory path of the Package repository.

            publish (bool): Flag indicating if the package should be published.

        Returns:
             Dict: Metadata of the package updated.
        """
        package_repository = Path(package_repository)

        if not package_repository.is_dir():
            raise NotADirectoryError("Package repository must be a valid directory")

        package_definition = load_package_repository(package_repository)

        # loading package
        package = self._load_element(
            package_definition["knowledge_package"], type_="package"
        )

        # loading resources
        resources = py_.map(
            package_definition["resources"],
            lambda resource: self._load_element(resource, type_="resource"),
        )

        # associating packages and resources.
        self._api.associate_package_resources(package, resources)

        if publish:
            package["metadata"] = self._api.publish(package)

        return package["metadata"]
