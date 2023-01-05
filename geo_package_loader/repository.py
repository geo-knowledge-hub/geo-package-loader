#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021-2023 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Package repository module for the GEO Knowledge Hub Package Loader."""

import json
from typing import Dict

from pydash import py_

from pathlib import Path


def _validate_package_reposistory(package_definition: Dict):
    """Validate package repository based on package definition."""

    def validate_obj(obj):
        # Validating metadata
        assert obj["metadata_file"].is_file(), "Invalid file"

        for resource in obj["files"]:
            assert resource.is_file(), "Invalid file"

    validate_obj(package_definition["knowledge_package"])
    py_.for_each(package_definition["resources"], lambda x: validate_obj(x))


def _fix_package_repository_definition(
    package_repository: Path, package_definition: Dict
):
    """Fix the path used in the package definition."""

    def fix_obj(obj):
        obj["metadata_file"] = package_repository / obj["metadata_file"]
        obj["files"] = py_.map(obj.get("files", []), lambda x: package_repository / x)

        return obj

    package_definition["knowledge_package"] = fix_obj(
        package_definition["knowledge_package"]
    )
    package_definition["resources"] = py_.map(
        package_definition["resources"], lambda x: fix_obj(x)
    )

    return package_definition


def _load_package_repository_metadata(package_definition: Dict):
    """Load metadata."""

    def load_metadata(obj):
        obj["metadata"] = json.load(obj["metadata_file"].open("r"))

        return obj

    package_definition["knowledge_package"] = load_metadata(
        package_definition["knowledge_package"]
    )
    package_definition["resources"] = py_.map(
        package_definition["resources"], lambda x: load_metadata(x)
    )

    return package_definition


def load_package_repository(package_repository: Path):
    """Parse and load a package repository."""
    # Loading package definition
    package_definition = py_.head(
        py_.filter(
            package_repository.iterdir(), lambda x: "knowledge-package.json" in x.name
        )
    )

    if not package_definition:
        raise RuntimeError("`knowledge-package.json` not found!")

    # Loading definition
    package_definition = json.load(package_definition.open("r"))

    # Fixing files path
    package_definition = _fix_package_repository_definition(
        package_repository, package_definition
    )

    # Validating
    _validate_package_reposistory(package_definition)

    # Load metadata
    _load_package_repository_metadata(package_definition)

    return package_definition
