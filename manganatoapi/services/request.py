import re

import requests

from manganatoapi.exceptions import NotFound

_404_NOT_FOUND = re.compile(
    r'<title>.*404 Not Found.*<\/title>', re.IGNORECASE
)


def get(url: str):
    """
    Sends a GET request to the provided URL and returns the response object.
    If the response contains a 404 Not Found error, a NotFound exception is
    raised.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        requests.Response: The response object from the GET request.

    Raises:
        NotFound: If the response contains a 404 Not Found error.
    """
    resp = requests.get(url, allow_redirects=False)

    if re.search(_404_NOT_FOUND, resp.text) or resp.status_code == 302:
        raise NotFound(f'{url} not found')

    return resp


def stream(url: str):
    """
    Streams the content from the provided URL, yielding the content type and
    length (if available), and then yielding the content in chunks.

    Args:
        url (str): The URL to stream the content from.

    Yields:
        Tuple[str, Optional[int]]: The content type and length (if available)
            of the streamed content.
        bytes: The content of the stream in 16 KB chunks.

    Raises:
        NotFound: If the content type of the response is 'text/html',
            indicating the image was not found.
    """
    headers = {'referer': 'https://manganato.com'}

    with requests.get(url, stream=True, headers=headers) as resp:
        try:
            ctype = resp.headers['content-type']
        except KeyError:
            ctype = None

        if ctype and ctype.startswith('text/html'):
            raise NotFound('Image Not Found')

        try:
            clength = resp.headers['content-length']
        except KeyError:
            clength = None

        yield ctype, clength

        for chunk in resp.iter_content(chunk_size=16 * 1024):
            yield chunk
