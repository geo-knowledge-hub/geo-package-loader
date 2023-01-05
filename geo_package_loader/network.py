#
# This file is part of GEO Knowledge Hub Package Loader.
# Copyright (C) 2021-2023 GEO Secretariat.
#
# GEO Knowledge Hub Package Loader is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Network module for the GEO Knowledge Hub Package Loader."""

import httpx
from pydash import py_

from .store import TokenStore


class HTTPXClient:

    _client_config = {"timeout": 12, "verify": False}
    """Default client config."""

    @classmethod
    def _proxy_request(cls, request_options):
        """Proxy a request to add the authentication access token."""

        # proxing the request with the authentication header
        service_access_token = TokenStore.get_token()

        if service_access_token:
            request_options = py_.merge(
                request_options or {},
                {"headers": {"Authorization": f"Bearer {service_access_token}"}},
            )
        return request_options

    @classmethod
    def set_client_config(cls, configuration):
        """Define the configuration for the ``httpx.Client``.

        Args:
            configuration (dict): ``httpx.Client`` configuration

        See:
            For more details about the ``httpx.Client``, please check the
            official documentation: https://www.python-httpx.org/api/#client
        """
        cls._client_config = configuration

    @classmethod
    def request(cls, method, url, **kwargs):
        """Synchronous HTTP request.

        Request an URL using the specified HTTP ``method``.
        Args:
            method (str): HTTP Method used to request (e.g. `GET`, `POST`, `PUT`, `DELETE`)

            url (str): URL that will be requested

            **kwargs (dict): Extra parameters to `httpx.request` method.

        Returns:
            httpx.Response: Request response.

        See:
            This method is built on top of ``httpx``. For more details of options available, please,
            check the official documentation: https://www.python-httpx.org/
        """
        with httpx.Client(**cls._client_config) as client:
            return client.request(method, url, **cls._proxy_request(kwargs or {}))

    @staticmethod
    def upload(method, url, file_path, **kwargs):
        """Download a file.

        Args:

            method (str): HTTP verb used to upload the data.

            url (str): URL to send the data.

            file_path (pathlib.Path): File path.

            kwargs (dict): Extra parameters to ``http.Client.request``.

        Returns:
            httpx.Response: Request response.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return HTTPXClient.request(
            method=method, url=url, data=file_path.open("rb"), **kwargs
        )
