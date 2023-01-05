#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021-2023 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Command-Line Interface for GEO Knowledge Hub Package Loader."""

import click

from time import sleep
from pathlib import Path

from geo_package_loader import PackageLoader


@click.group()
@click.version_option()
def cli():
    """Knowledge Package loader."""


@cli.command()
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.option("-ph", "--publish", is_flag=True, default=False)
@click.option(
    "-p",
    "--packages-api",
    required=True,
    type=str,
    default="https://127.0.0.1:5000/api/packages",
    help="Invenio REST API base URL.",
)
@click.option(
    "-r",
    "--records-api",
    required=True,
    type=str,
    default="https://127.0.0.1:5000/api/records",
    help="Invenio REST API base URL.",
)
@click.option(
    "-t", "--access-token", required=False, type=str, help="User Personal Access Token."
)
@click.option(
    "-k",
    "--knowledge-package-repository",
    required=True,
    type=str,
    help="Directory where the knowledge-package.json file is defined.",
)
def load(
    verbose,
    publish,
    packages_api,
    records_api,
    access_token,
    knowledge_package_repository,
):
    """Load the metadata and resources of a Knowledge Package."""

    knowledge_package_repository = Path(knowledge_package_repository)

    if verbose:
        click.secho(
            "Packages API....................: ", nl=False, bold=True, fg="green"
        )
        click.secho(packages_api)

        click.secho(
            "Records API.....................: ", nl=False, bold=True, fg="green"
        )
        click.secho(records_api)

        click.secho(
            "Personal Access Token...........: ", nl=False, bold=True, fg="green"
        )
        click.secho(access_token)

        click.secho(
            "Knowledge Package repository....: ", nl=False, bold=True, fg="green"
        )
        click.secho(knowledge_package_repository.name)

    click.secho(
        "Configuring the client to upload content to the GEO Knowledge Hub\n",
        nl=False,
        bold=True,
        fg="green",
    )

    loader = PackageLoader(
        access_token=access_token,
        package_api=packages_api,
        record_api=records_api,
    )

    sleep(1)
    click.secho("Done!", bold=True, fg="green")

    click.secho(
        "Creating the package and its resources\n",
        nl=False,
        bold=True,
        fg="green",
    )

    try:
        loader.service.load_package(
            package_repository=knowledge_package_repository, publish=publish
        )

        sleep(1)
        click.secho("Finished!", bold=True, fg="green")
    except Exception as e:
        click.secho("Error to load the package!", bold=True, fg="red")
        click.secho(str(e), bold=True, fg="red")
