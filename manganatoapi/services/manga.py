import re
from urllib.parse import urljoin

from parsel import Selector, SelectorList

from manganatoapi import utils
from manganatoapi.services import request

MANGA_UPDATES_URL = 'https://manganato.com/genre-all'
MANGA_INFO_URLS = {
    'cu': 'https://chapmanganato.to',
    'mu': 'https://manganato.com',
}


def updates(page: int, base_url='/mangas/'):
    """
    Retrieves a list of recently updated manga from the Manganato website.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a
            manga and contains the following keys:
            - 'url': The URL of the manga page.
            - 'cover': The URL of the manga cover image.
            - 'title': The title of the manga.
            - 'views': The number of views for the manga.
            - 'last_chapter': The title of the most recently updated chapter.
            - 'last_update': The date the manga was last updated.
            - 'author': The name of the manga's author.
    """
    resp = request.get(
        MANGA_UPDATES_URL + f'{"/%s" % page if page > 1 else ""}'
    )
    select = utils.get_selector(resp.text)

    result = []

    for manga in select("//div[contains(@class, 'content-genres-item')]"):
        url = utils.make_url(base_url, manga.xpath('.//a/@href').get())

        if not url:
            continue

        author = manga.xpath(
            './/span[@class="genres-item-author"]/text()'
        ).get()

        if author:
            author = utils.strip_list(author.split(','))

        result.append(
            {
                'url': url,
                'cover': manga.xpath('.//img/@src').get(),
                'title': manga.xpath('.//h3/a/text()').get(),
                'author': author,
                'views': manga.xpath(
                    './/span[@class="genres-item-view"]/text()'
                ).get(),
                'last_chapter': manga.xpath(
                    './/a[contains(@class, "genres-item-chap")]/text()'
                ).get(),
                'last_update': manga.xpath(
                    './/span[@class="genres-item-time"]/text()'
                ).get(),
            }
        )

    return result


def _process_chapters(chapters: SelectorList[Selector]):
    """
    Processes a list of chapter elements and returns a list of dictionaries
    representing the chapters.

    Args:
        chapters (SelectorList[Selector]): A list of Selector objects
            representing the chapter elements.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a
            chapter and contains the following keys:
            - 'url': The URL of the chapter page.
            - 'title': The title of the chapter.
            - 'number': The chapter number.
    """
    result = []

    for ch in chapters:
        ch_url = ch.xpath('./@href').get()

        if not ch_url:
            continue

        ch_url_encoded = utils.encode_url(ch_url)

        result.append(
            {
                'url': f'/chapters/{ch_url_encoded}',
                'title': ch.xpath('./text()').get(),
                'number': utils.get_chapter_number(ch_url),
            }
        )

    return result


def info(manga: str, prefix: str):
    """
    Retrieves information about a manga based on the provided manga name and
    prefix.

    Args:
        manga (str): The name of the manga to retrieve information for.
        prefix (str): The prefix to use for the manga information URL.

    Returns:
        dict: A dictionary containing the following keys:
            - 'title': The title of the manga.
            - 'cover': The URL of the manga's cover image.
            - 'genres': A list of the manga's genres.
            - 'status': The status of the manga (e.g. "Ongoing", "Completed").
            - 'author': A list of the manga's authors.
            - 'views': The number of views for the manga.
            - 'last_update': The date of the last update for the manga.
            - 'description': A description of the manga.
            - 'chapters': A list of dictionaries, where each dictionary
                represents a chapter and contains the following keys:
                - 'url': The URL of the chapter page.
                - 'title': The title of the chapter.
                - 'number': The chapter number.
    """
    url = urljoin(MANGA_INFO_URLS[prefix], manga)
    resp = request.get(url)
    select = utils.get_selector(resp.text)

    return {
        'title': select("//div[@class='story-info-right']/h1/text()").get(),
        'cover': select(
            "//span[contains(@class, 'info-image')]//img/@src"
        ).get(),
        'genres': select(
            "//td[text()='Genres :']/following-sibling::td/a/text()"
        ).getall(),
        'status': select(
            "//td[text()='Status :']/following-sibling::td/text()"
        ).get(),
        'author': select(
            "//td[text()='Author(s) :']/following-sibling::td/a/text()"
        ).getall(),
        'views': select(
            "//div[@class='story-info-right-extent']//span[text()='View :']"
            '/following-sibling::span/text()'
        ).get(),
        'last_update': select(
            "//div[@class='story-info-right-extent']//span[text()='Updated :']"
            '/following-sibling::span/text()'
        ).get(),
        'description': utils.normalize_text(
            ''.join(
                select(
                    "//div[contains(@class, 'panel-story-info-description')]"
                    '//text()'
                ).getall()
            )
        ),
        'chapters': _process_chapters(
            select("//ul[contains(@class, 'row-content-chapter')]//a")
        ),
    }


def images(chapter: str):
    """
    Retrieves the image URLs for a given chapter of a manga.

    Args:
        chapter (str): The URL of the chapter page.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents
            an image and contains the following keys:
            - 'order': The order of the image in the chapter.
            - 'url': The URL of the image.
    """
    decoded_url = utils.decode_url(chapter)
    resp = request.get(decoded_url)
    select = utils.get_selector(resp.text)

    return [
        {'order': i, 'url': f'/images/{utils.encode_url(url)}'}
        for i, url in enumerate(
            select(
                "//div[contains(@class, 'container-chapter-reader')]//img/@src"
            ).getall()
        )
    ]


def search(query: str, page: int):
    """
    Searches for manga based on the provided query and page number.

    Args:
        query (str): The search query.
        page (int): The page number to retrieve.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a
            manga and contains the following keys:
            - 'url': The URL of the manga.
            - 'cover': The URL of the manga's cover image.
            - 'title': The title of the manga.
            - 'author': The author of the manga.
            - 'last_update': The date of the last update for the manga.
            - 'views': The number of views for the manga.
    """
    query = re.sub(r'[^a-zA-Z0-9]', '_', query)
    url = urljoin(MANGA_UPDATES_URL, f'search/story/{query}')

    if page > 1:
        url += f'?page={page}'

    resp = request.get(url)
    select = utils.get_selector(resp.text)

    result = []
    for manga in select("//div[@class='search-story-item']"):
        url = utils.make_url('/mangas/', manga.xpath('.//a/@href').get())

        if not url:
            continue

        last_update = manga.xpath(
            ".//span[contains(@class, 'item-time')]/text()"
        ).get()

        if last_update:
            last_update = re.sub(
                r'\b[Uu][Pp][Dd][Aa][Tt][Ee][Dd]\s*[:]\s*', '', last_update
            )

        views = manga.xpath(
            ".//span[contains(@class, 'item-time')][2]/text()"
        ).get()

        if views:
            views = re.sub(r'\b[Vv][Ii][Ee][Ww]\s*[:]\s*', '', views)

        author = manga.xpath(
            ".//span[contains(@class, 'item-author')]/text()"
        ).get()

        if author:
            author = utils.strip_list(author.split(','))

        result.append(
            {
                'url': url,
                'cover': manga.xpath('.//img/@src').get(),
                'title': manga.xpath('.//h3/a/text()').get(),
                'author': author,
                'last_update': last_update,
                'views': views,
            }
        )

    return result
