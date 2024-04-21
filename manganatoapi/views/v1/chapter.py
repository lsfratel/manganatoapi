from __future__ import annotations

import binascii
import typing as t

from restcraft.core import JSONResponse, Request, View
from restcraft.core.di import inject

from ... import utils

if t.TYPE_CHECKING:
    from ...services.manga import MangaService


class ChapterView(View):
    """
    Defines the `ChapterView` class, which is a view for handling requests to
    the `/chapters/<chapter>` route.

    This view is responsible for fetching and returning images urls
    for a specific chapter.
    """

    route = '/v1/chapters/<chapter:str>'
    methods = ['GET']

    @inject
    def handler(self, req: Request, service: MangaService) -> JSONResponse:
        images = service.images(req.params['chapter'])

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
