from __future__ import annotations

import typing as t

from restcraft.core.middleware.middleware import Middleware

if t.TYPE_CHECKING:
    from restcraft.core import Request, Response


class SnakeCaseToCamelCase(Middleware):
    """
    This middleware is responsible for transforming the response body from
    snake_case to camelCase.

    It recursively traverses the response body, converting all keys from
    snake_case to camelCase.
    """

    def key_to_camel_case(self, key: str) -> str:
        """
        Converts a snake_case string to camelCase.

        Args:
            key (str): The snake_case string to convert.

        Returns:
            str: The converted camelCase string.
        """

        c = key.split('_')
        return c[0].lower() + ''.join(x.title() for x in c[1:])

    def snake_to_camel(self, body: dict) -> dict[str, t.Any]:
        """
        Recursively traverses the response body, converting all keys from
        snake_case to camelCase.

        Args:
            body (dict): The dictionary to be converted from snake_case to
                camelCase.

        Returns:
            dict: The converted dictionary with camelCase keys.
        """

        new_body = {}

        for k, v in body.items():
            key = self.key_to_camel_case(k)
            if isinstance(v, dict):
                new_body[key] = self.snake_to_camel(v)
            elif isinstance(v, list):
                new_body[key] = [
                    self.snake_to_camel(item)
                    if isinstance(item, dict)
                    else item
                    for item in v
                ]
            else:
                new_body[key] = v

        return new_body

    def after_handler(self, _: Request, res: Response) -> None:
        """
        This method is called after the main request handler.
        """

        if not isinstance(res.body, dict):
            return

        res.set_body = self.snake_to_camel(res.body)
