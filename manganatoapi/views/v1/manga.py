from restcraft.core import JSONResponse, Request, View

from manganatoapi import exceptions, utils
from manganatoapi.services import manga


class MangaView(View):
    """
    Defines the `MangaView` class, which is a view for handling requests to the
    `/mangas` route.

    This view is responsible for fetching and returning the latest manga
    updates.
    """

    route = '/v1/mangas'
    methods = ['GET']

    def handler(self, req: Request) -> JSONResponse:
        page = int(req.query.get('page', 1))
        search = req.query.get('q', None)

        if search:
            updates = manga.search(search, page)
        else:
            updates = manga.updates(page)

        return utils.success_response(
            'Latest manga updates fetched successful.', payload=updates
        )


class MangaInfoView(View):
    """
    Defines the `MangaInfoView` class, which is a view for handling requests to
    the `/mangas/<manga>` route.

    This view is responsible for fetching and returning detailed information
    about a specific manga.
    """

    route = '/v1/mangas/<manga>'
    methods = ['GET']

    def handler(self, req: Request) -> JSONResponse:
        manga_prefix, _, manga_id = req.params['manga'].partition('-')
        manga_info = manga.info(manga_id, manga_prefix)

        return utils.success_response(
            'Latest manga info fetched successful.', payload=manga_info
        )

    def on_exception(self, req: Request, exc: Exception) -> JSONResponse:
        if not isinstance(exc, exceptions.NotFound):
            raise exc

        return utils.error_response(
            status_code=404,
            message='Manga not found.',
            exception_code='MANGA_NOT_FOUND',
        )
