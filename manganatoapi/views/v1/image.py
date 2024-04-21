from __future__ import annotations

import binascii
import typing as t

from restcraft.core import FileResponse, JSONResponse, Request, View
from restcraft.core.di import inject

from ... import exceptions, utils

if t.TYPE_CHECKING:
    from ...services.image import ImageService


class ImageView(View):
    """
    Defines the `ImageView` class, which is a view for handling requests to
    the `/images/<image>` route.

    It is responsible for retrieving and serving the requested chapter image.
    """

    route = '/v1/images/<image:str>'
    methods = ['GET']

    @inject
    def handler(self, req: Request, service: ImageService) -> FileResponse:
        filename, headers, generator = service.get(req.params['image'])

        if filename == '':
            filename = 'unknown.jpg'

        return FileResponse(generator, filename=filename, headers=headers)

    def on_exception(self, _: Request, exc: Exception) -> JSONResponse:
        if not isinstance(exc, (exceptions.NotFound, binascii.Error)):
            raise exc

        return utils.error_response(
            message='Image not found.',
            status_code=404,
            exception_code='IMAGE_NOT_FOUND',
        )
