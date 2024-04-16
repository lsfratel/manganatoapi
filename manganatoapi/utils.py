import base64
import typing as t
from urllib.parse import urljoin, urlparse

import parsel
from restcraft.core import JSONResponse


def make_url(base_url: str, manga_url: str | None):
    """
    Constructs a URL for a manga page based on the provided base URL and manga
    URL.

    If the manga URL is not provided, this function returns `None`.

    The function parses the provided manga URL and constructs a new URL path
    based on the domain of the manga URL. If the domain is 'chapmanganato.to',
    the path is prefixed with 'cu-'. Otherwise, the path is prefixed with
    'mu-'.

    The constructed URL is then joined with the provided base URL and returned.

    Args:
        base_url (str): The base URL to use for constructing the final URL.
        manga_url (str | None): The URL of the manga page.

    Returns:
        str | None: The constructed URL, or `None` if the manga URL was not
            provided.
    """
    if not manga_url:
        return None

    url = urlparse(manga_url)

    if url.netloc == 'chapmanganato.to':
        path = f'cu-{url.path.lstrip("/")}'
    else:
        path = f'mu-{url.path.lstrip("/")}'

    return urljoin(base_url, path)


def success_response(message: str, payload: t.Any):
    """
    Constructs a JSON response with a 'SUCCESS' code, the provided
    message, and the provided data.

    Args:
        message (str): The message to include in the response.
        data (t.Any): The data to include in the response.

    Returns:
        JSONResponse: The constructed JSON response.
    """
    response = {
        'code': 'SUCCESS',
        'message': message,
        'data': payload,
    }

    return JSONResponse(response)


def error_response(
    message: str, status_code: int, exception_code: str, payload: t.Any = None
):
    """
    Constructs a JSON response with the provided error message, status code,
    and exception code.

    Args:
        message (str): The error message to include in the response.
        status_code (int): The HTTP status code to use for the response.
        exception_code (str): The exception code to include in the response.
        payload (t.Any, optional): Any additional data to include in the
            response. Defaults to None.

    Returns:
        JSONResponse: The constructed JSON response.
    """
    response = {
        'code': exception_code,
        'message': message,
        **(payload or {}),
    }

    return JSONResponse(response, status_code=status_code)


def get_selector(resp_text: str):
    """
    Constructs a Parsel selector from the provided response text.

    Args:
        resp_text (str): The response text to create the selector from.

    Returns:
        parsel.Selector: The constructed Parsel selector.
    """
    return parsel.Selector(resp_text).xpath


def get_chapter_number(chapter_url: str | None):
    """
    Extracts the chapter number from the provided chapter URL.

    Args:
        chapter_url (str | None): The URL of the chapter.

    Returns:
        float: The chapter number extracted from the URL.
    """
    if not chapter_url:
        return
    return float(chapter_url.split('/')[-1].split('-')[-1])


def encode_url(url: str):
    """
    Encodes a URL by converting it to bytes, base64 encoding the bytes, and
    then decoding the base64 bytes back to a string.

    Args:
        url (str): The URL to encode.

    Returns:
        str: The base64-encoded URL.
    """
    url_bytes = url.encode('utf-8')
    base64_bytes = base64.urlsafe_b64encode(url_bytes)
    return base64_bytes.decode('utf-8')


def decode_url(encoded_url: str):
    """
    Decodes a base64-encoded URL back to its original string form.

    Args:
        encoded_url (str): The base64-encoded URL to decode.

    Returns:
        str: The original URL as a string.
    """
    base64_bytes = encoded_url.encode('utf-8')
    url_bytes = base64.urlsafe_b64decode(base64_bytes)
    return url_bytes.decode('utf-8')


def strip_list(lst: list[str]):
    """
    Strips leading and trailing whitespace from each string in the provided
    list.

    Args:
        lst (list[str]): The list of strings to strip.

    Returns:
        list[str]: A new list with the strings stripped of leading and trailing
            whitespace.
    """
    return [x.strip() for x in lst]
