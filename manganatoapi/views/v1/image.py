import binascii

from restcraft.core import FileResponse, JSONResponse, Request, View

from manganatoapi import exceptions, utils
from manganatoapi.services import image


class ImageView(View):
    """
    Defines the `ImageView` class, which is a view for handling requests to
    the `/images/<image>` route.

    It is responsible for retrieving and serving the requested chapter image.
    """

    route = '/v1/images/<image:str>'
    methods = ['GET']

    def handler(self, req: Request) -> FileResponse:
        filename, headers, generator = image.get(req.params['image'])

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
