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
        page = 1
        search = None

        if req.query:
            page = req.query.get('page', default=1, type=int)
            search = req.query.get('q', type=str)

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

    def before_handler(self, req: Request) -> None:
        prefix, _, manga = req.params['manga'].partition('-')
        req.set_params = {'prefix': prefix,'manga': manga}

    def handler(self, req: Request) -> JSONResponse:
        manga_info = manga.info(
            prefix=req.params['prefix'], manga=req.params['manga']
        )

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
