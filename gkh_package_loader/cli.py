#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Command-Line Interface for GEO Knowledge Hub Package Loader."""

import json
import os

import click
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning warnings from urllib3.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def create_record_draft(metadata, invenio_rest_api, access_token):
    """Create a new record draft through InvenioRDM REST API.

    Args:
        metadata (dict): The resource metadata.
        invenio_rest_api (str): Base URL for InvenioRDM REST API.
        access_token (str): A valid bearer token to be used to create the new record.

    Returns:
        dict: The record draft metadata returned by InvenioRDM.

    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If resource file does not exist.
    """
    url = '/'.join((invenio_rest_api.strip('/'), 'records'))

    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {access_token}'
    }

    response = requests.post(url=url,
                             data=json.dumps(metadata),
                             headers=headers,
                             verify=False)

    rec = response.json()

    return rec


def publish_record(record_metadata, access_token):
    """Publish record using InvenioRDM REST API.

    Args:
        record_metadata (dict): The record draft metadata with links to publish route.
        access_token (str): A valid bearer token to be used to create the new record.

    Returns:
        dict: The record metadata returned by InvenioRDM.

    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If resource file does not exist.
    """
    url = record_metadata['links']['publish']

    headers = {
        'authorization': f'Bearer {access_token}'
    }

    response = requests.post(url=url,
                             headers=headers,
                             verify=False)

    return response.json()



def upload_file(resource_filename, access_token, record_metadata):
    """Upload a file using InvenioRDM REST API.

    Args:
        resource_filename (str): The file name with full path for the resource to be uploaded.
        access_token (str): A valid bearer token to be used to upload the resource file.
        record_metadata (dict): Record draft metadata with the ``links`` key.

    Returns:
        dict: The record metadata returned by InvenioRDM.

    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If resource file does not exist.
    """
    if not os.path.exists(resource_filename):
        raise ValueError(f'Resource file does not exist: "{resource_filename}".')

    base_filename = os.path.basename(resource_filename)

    # register a file upload
    resource_metadata_url = record_metadata['links']['files']

    resource_metadata_headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {access_token}'
    }

    resource_metadata_response = requests.post(url=resource_metadata_url,
                                               data=f'[{{"key": "{base_filename}"}}]',
                                               headers=resource_metadata_headers,
                                               verify=False)

    resource_metadata = resource_metadata_response.json()

    # upload the file
    content_url = resource_metadata['entries'][0]['links']['content']

    content_headers = {
        'content-type': 'application/octet-stream',
        'authorization': f'Bearer {access_token}'
    }

    content_response = requests.put(url=content_url,
                                    data=open(resource_filename, 'rb'),
                                    headers=content_headers,
                                    verify=False)

    content_metadata = content_response.json()

    # commit the uploaded file
    commit_url = content_metadata['links']['commit']

    commit_headers = {
        'authorization': f'Bearer {access_token}'
    }

    commit_response = requests.post(url=commit_url,
                                    headers=commit_headers,
                                    verify=False)

    return commit_response.json()


def add_related_identifiers(id, identifiers, invenio_rest_api, access_token):
    """Add related identifiers to an existing record.

    Args:
        id (str): The record identifier.
        identifiers (list): The list of related resources.
        invenio_rest_api (str): Base URL for InvenioRDM REST API.
        access_token (str): A valid bearer token to be used to create the new record.

    Returns:
        dict: The record metadata returned after updating it.

    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If resource file does not exist.
    """
    # create a draft record from a published record
    url = '/'.join((invenio_rest_api.strip('/'), 'records', id, 'draft'))

    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {access_token}'
    }

    response = requests.post(url=url, headers=headers, verify=False)

    draft_record = response.json()

    # add the related identifiers to the beginning of an
    # already existing list of identifiers
    if 'related_identifiers' not in draft_record['metadata']:
        draft_record['metadata']['related_identifiers'] = []

    identifiers.extend(draft_record['metadata']['related_identifiers'])

    draft_record['metadata']['related_identifiers'] = identifiers

    # update the draft record with the new related_identifiers
    response = requests.put(url=url,
                            data=json.dumps(draft_record),
                            headers=headers,
                            verify=False)

    draft_record = response.json()

    # re-publish the record
    pub_record = publish_record(draft_record, access_token)

    return pub_record


@click.group()
@click.version_option()
def cli():
    """Knowledge Package loader."""


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-u', '--url', required=True, type=str,
              default='https://127.0.0.1:5000/api',
              help='Invenio REST API base URL.')
@click.option('-t', '--access-token', required=False, type=str,
              help='User Personal Access Token.')
@click.option('-k', '--knowledge-package', required=True, type=click.File('rb'),
              help='A knowledge package index file name. The file entries are' \
                   'key-value pairs with the name of a metadata file as keys' \
                   'and resources file as arrays.')
@click.option('-r', '--resources-dir', required=False, type=str,
              help='Knowledge Pakcage resources directory.')
def load(verbose, url, access_token, knowledge_package, resources_dir):
    """Load the metadata and resources of a Knowledge Package."""
    kpackage = json.load(knowledge_package)

    if verbose:
        click.secho('Invenio REST API.....: ', nl=False, bold=True, fg='green')
        click.secho(url)

        click.secho('Personal Access Token: ', nl=False, bold=True, fg='green')
        click.secho(access_token)

        click.secho('Knowledge Package....: ', nl=False, bold=True, fg='green')
        click.secho(knowledge_package.name)

        click.secho('Resources directory..: ', nl=False, bold=True, fg='green')
        click.secho(resources_dir)

    # read all the metadata from the knowledge package and its components
    click.secho('Reading metadata from the knowledge package and its components... ',
                nl=False, bold=True, fg='green')

    metadata_filename = os.path.join(resources_dir, kpackage['knowledge_package']['metadata_file'])

    if not os.path.exists(metadata_filename):
        raise FileExistsError(f'Knowledge Package metadata file does not exist: "{metadata_filename}".')

    kpackage['knowledge_package']['metadata'] = json.load(open(metadata_filename))

    for component in kpackage['components']:
        metadata_filename = os.path.join(resources_dir, component['metadata_file'])

        if not os.path.exists(metadata_filename):
            raise FileExistsError(f'Application component metadata file does not exist: "{metadata_filename}".')

        component["metadata"] = json.load(open(metadata_filename))

    click.secho('ok!', bold=True, fg='green')

    # create the draft record for the knowledge package,
    # then upload all its associated resources and
    # finally publish it
    click.secho('Creating knowledge package: ' \
                f'"{kpackage["knowledge_package"]["metadata"]["metadata"]["title"]}"...',
                bold=True, fg='yellow')
    click.secho('\tcreating record draft... ', nl=False)

    knowledge_package_record = create_record_draft(kpackage['knowledge_package']['metadata'], url, access_token)

    click.secho('ok!', bold=True, fg='green')
    click.secho('\tuploading files... ', nl=False)

    for resource in kpackage['knowledge_package']['resources']:
        resource_filename = os.path.join(resources_dir, resource)
        upload_file(resource_filename, access_token, knowledge_package_record)

    click.secho('ok!', bold=True, fg='green')
    click.secho('\tpublishing record... ', nl=False)

    knowledge_package_record = publish_record(knowledge_package_record, access_token)

    knowledge_package_doi = knowledge_package_record['pids']['doi']['identifier']

    click.secho('ok!\nKnowledge Package created!\n', bold=True, fg='green')
    click.secho('Creating components... ', bold=True, fg='yellow')

    # for each component of the knowledge package:
    # - link it to the knowledge package through the doi;
    # - create a draft record for the component;
    # - upload all its associated resources;
    # - publish the component.
    # - add the component in the related_identifiers list for the knowledge package
    knowledge_package_related_identifiers = []

    for component in kpackage['components']:
        component_metadata = component['metadata']

        if 'related_identifiers' not in component_metadata['metadata']:
            component_metadata['metadata']['related_identifiers'] = []

        related_identifier = {
            "identifier": knowledge_package_doi,
            "scheme": "doi",
            "relation_type": "ispartof",
            "resource_type": {
                "type": "knowledge"
            }
        }

        # link the component to the knowledge package through the doi
        component_metadata['metadata']['related_identifiers'].insert(0, related_identifier)

        # create the component draft record
        click.secho(f'\tcreating component: "{component_metadata["metadata"]["title"]}"... ',
                    bold=True, fg='yellow')
        click.secho('\t\tcreating draft record... ', nl=False)

        component_record = create_record_draft(component_metadata, url, access_token)

        click.secho('ok!', bold=True, fg='green')
        click.secho('\t\tuploading files... ', nl=False)

        # upload files associated to the component
        for resource in component['resources']:
            resource_filename = os.path.join(resources_dir, resource)
            upload_file(resource_filename, access_token, component_record)

        click.secho('ok!', bold=True, fg='green')
        click.secho('\t\tpublishing component... ', nl=False)

        # publish the component
        component_record = publish_record(component_record, access_token)

        knowledge_package_component_relation = {
            "identifier": component_record['pids']['doi']['identifier'],
            "scheme": "doi",
            "relation_type": "haspart",
            "resource_type": component_record['metadata']["resource_type"]
        }

        knowledge_package_related_identifiers.insert(0, knowledge_package_component_relation)

        click.secho('ok!', bold=True, fg='green')
        click.secho(f'\tcomponent: "{component_metadata["metadata"]["title"]}" created!\n',
                    bold=True, fg='green')

    click.secho('Components created!\n', bold=True, fg='green')
    click.secho('Updating the knowledge package list of related identifiers... ',
                nl=False, bold=True, fg='yellow')

    # update the knowledge package with related identifiers
    add_related_identifiers(knowledge_package_record['id'],
                            knowledge_package_related_identifiers,
                            url, access_token)

    click.secho('ok!', bold=True, fg='green')

