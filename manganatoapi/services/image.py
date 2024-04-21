from __future__ import annotations

import os
import typing as t
from urllib.parse import unquote, urlparse

from restcraft.core.di import inject

from .. import utils

if t.TYPE_CHECKING:
    from .request import RequestService


class ImageService:
    @classmethod
    @inject
    def get(cls, encoded_url: str, request: RequestService):
        """
        Retrieves the image file and its metadata from the provided encoded
        URL.

        Args:
            encoded_url (str): The encoded URL of the image to retrieve.

        Returns:
            tuple: A tuple containing the following:
                - filename (str): The filename of the image.
                - headers (dict): A dictionary of HTTP headers for the image,
                    including content-length and content-type.
                - stream (generator): A generator that yields the image data in
                    chunks.
        """
        url = utils.decode_url(encoded_url)
        parsed_url = urlparse(url)

        stream = request.stream(url)

        ctype, clength = next(stream)

        headers = {}

        if clength:
            headers['content-length'] = clength

        if ctype:
            headers['content-type'] = ctype

        filename = os.path.basename(unquote(parsed_url.path))

        return filename, headers, stream
