#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021-2023 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Base API client for the GEO Knowledge Hub services."""

from pydash import py_

from pathlib import Path
from typing import Dict, List

from .network import HTTPXClient


def _validate_type(type_):
    """Check if type is valid."""
    if not type_ or type_ not in ["package", "resource"]:
        raise RuntimeError("Invalid draft type")


def _validate_url(url):
    """Check if a url is valid."""
    if not url:
        raise RuntimeError("Metadata don't have the correct link for this operation.")


class GEOKnowledgeHubApi:
    def __init__(self, package_api: str, record_api: str):
        self._package_api = package_api
        self._record_api = record_api

    #
    # Properties
    #
    @property
    def package_api(self):
        return self._package_api

    @property
    def record_api(self):
        return self._record_api

    #
    # Base methods
    #
    def _create_draft(self, metadata, address):
        """Create draft in the GEO Knowledge Hub."""
        response = HTTPXClient.request("POST", address, json=metadata)
        response.raise_for_status()

        return response.json()

    def _upload_files(self, files, address):
        """Upload files to the GEO Knowledge Hub."""
        # Defining files
        files_map = {x.name: x for x in files}
        file_keys = py_.map(files, lambda x: dict(key=x.name))

        response = HTTPXClient.request("POST", address, json=file_keys)
        response.raise_for_status()

        file_entries = py_.get(response.json(), "entries", [])

        for file_entry in file_entries:
            file_key = py_.get(file_entry, "key")
            file_path = files_map[file_key]

            file_content_link = py_.get(file_entry, "links.content")
            file_commit_link = py_.get(file_entry, "links.commit")

            # uploading file
            response = HTTPXClient.upload("PUT", file_content_link, file_path)
            response.raise_for_status()

            # committing file
            response = HTTPXClient.request("POST", file_commit_link)
            response.raise_for_status()

            del files_map[file_key]

        # validating if all files were uploaded
        assert len(files_map.keys()) == 0, "Error to upload the data"

    def _load_element(self, address):
        """Load element (Package or Resource) from the GEO Knowledge Hub."""
        response = HTTPXClient.request("GET", address)
        response.raise_for_status()

        return response.json()

    def _reserve_doi(self, address):
        """Reserve a DOI."""
        response = HTTPXClient.request("POST", address)
        response.raise_for_status()

        return response.json()

    def _associate_resources_package_context(self, resources, address):
        """Associate resources to the package context."""
        response = HTTPXClient.request("POST", address, json=dict(records=resources))
        response.raise_for_status()

    def _associate_resources_package_version(self, resources, address):
        """Associate resources to the current package version."""
        response = HTTPXClient.request("POST", address, json=dict(resources=resources))
        response.raise_for_status()

    def _publish_element(self, address):
        """Publish an element."""
        response = HTTPXClient.request("POST", address)
        response.raise_for_status()

        return response.json()

    #
    # High-Level methods.
    #
    def create_draft(self, metadata: Dict, type_: str) -> Dict:
        """Create a draft (Package or Resource) in the GEO Knowledge Hub.

        Args:
            metadata (Dict): Metadata of the resource that will be created.

            type_ (str): Type of the resource to be created (`package` or `resource`).
        Returns:
            Dict: Metadata from the GEO Knowledge Hub service.
        """
        _validate_type(type_)

        operation_url = self._package_api if type_ == "package" else self._record_api
        return self._create_draft(metadata, operation_url)

    def upload_files(
        self,
        metadata: Dict,
        files: List[Path],
        type_: str,
    ):
        """Upload files to an element (Package or Resource).

        Args:
            metadata (Dict): Metadata from the GEO Knowledge Hub service.

            files (List[Path]): List with path of the files to be uploaded.

            type_ (str): Type of the resource to be created (`package` or `resource`).
        Returns:
            Dict: Metadata from the GEO Knowledge Hub service.
        """
        _validate_type(type_)

        operation_url = py_.get(metadata, "links.files")
        _validate_url(operation_url)

        # uploading file
        self._upload_files(files, operation_url)

        # reloading package
        operation_url = py_.get(metadata, "links.self")
        return self._load_element(operation_url)

    def reserve_doi(self, metadata: Dict) -> Dict:
        """Reserve a DOI for a Package or Resource.

        Args:
            metadata (Dict): Metadata from the GEO Knowledge Hub service.
        Returns:
            Dict: Metadata from the GEO Knowledge Hub service.
        """
        operation_url = py_.get(metadata, "links.reserve_doi")
        _validate_url(operation_url)

        return self._reserve_doi(operation_url)

    def associate_package_resources(
        self, package_metadata: Dict, resources_metadata: List[Dict]
    ) -> Dict:
        """Associate a Package to a list of Resources.

        Args:
            package_metadata (Dict): Package metadata.

            resources_metadata (List[Dict]): List of resources metadata.
        Returns:
             Dict: Metadata of the package updated.
        """
        records = py_.map(resources_metadata, lambda x: dict(id=x["metadata"]["id"]))

        # associating resources to the package context.
        operation_url = py_.get(package_metadata, "metadata.links.context_associate")
        self._associate_resources_package_context(records, operation_url)

        # associating resources to the current version of the package
        operation_url = py_.get(package_metadata, "metadata.links.resources")
        self._associate_resources_package_version(records, operation_url)

        # updating the package
        operation_url = py_.get(package_metadata, "metadata.links.self")
        return self._load_element(operation_url)

    def publish(self, metadata: Dict) -> Dict:
        """Publish a complete Package or Resource.

        Args:
            metadata (Dict): Metadata from the GEO Knowledge Hub service.
        Returns:
            Dict: Metadata from the GEO Knowledge Hub service.
        """
        operation_url = py_.get(metadata, "links.publish")
        _validate_url(operation_url)

        return self._publish_element(operation_url)
