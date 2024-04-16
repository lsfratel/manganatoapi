import os

DEBUG = os.environ.get('DEBUG', 'true').lower() in ('true', '1')

VIEWS = {
    'manganatoapi.views.v1.manga',
    'manganatoapi.views.v1.chapter',
    'manganatoapi.views.v1.image',
}

MIDDLEWARES = {
    'manganatoapi.middlewares.camel_case.SnakeCaseToCamelCase',
}


try:
    from .local_settings import *  # type: ignore # noqa: F403
except ImportError:
    pass
