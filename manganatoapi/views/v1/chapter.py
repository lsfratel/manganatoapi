import binascii

from restcraft.core import JSONResponse, Request, View

from manganatoapi import utils
from manganatoapi.services import manga


class ChapterView(View):
    """
    Defines the `ChapterView` class, which is a view for handling requests to
    the `/chapters/<chapter>` route.

    This view is responsible for fetching and returning images urls
    for a specific chapter.
    """

    route = r'^/v1/chapters/(?P<chapter>[^/]+)$'
    methods = ['GET']

    def handler(self, req: Request) -> JSONResponse:
        images = manga.images(req.params['chapter'])

        return utils.success_response(
            'Chapter images fetched successful.', payload=images
        )

    def on_exception(self, req: Request, exc: Exception) -> JSONResponse:
        if not isinstance(exc, binascii.Error):
            raise exc

        return utils.error_response(
            message='Chapter not found.',
            status_code=404,
            exception_code='CHAPTER_NOT_FOUND',
        )
