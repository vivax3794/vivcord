"""Errors generated by the lib."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vivcord._typed_dicts import ErrorResponse


# https://discord.com/developers/docs/topics/opcodes-and-status-codes#http-http-response-codes


class HttpError(Exception):
    """A generic http error."""

    def __init__(self, http_code: int, raw_error: ErrorResponse) -> None:
        """
        Create error.

        Args:
            http_code (int): This errors http code
            raw_error (ErrorResponse): Raw discord error
        """
        super().__init__(raw_error)
        self.http_code = http_code
        self.raw_error = raw_error


class HttpUnauthorizedError(HttpError):
    """You must login."""


class HttpForbiddenError(HttpError):
    """You are not allowed to."""


class HttpNotFoundError(HttpError):
    """Could not find that."""


class HttpMethodNotAllowedError(HttpError):
    """You cant to that to this."""


class HttpToManyRequestsError(HttpError):
    """You are hitting a ratelimit."""


HTTP_ERRORS: dict[int, type[HttpError]] = {
    400: HttpError,
    401: HttpUnauthorizedError,
    403: HttpForbiddenError,
    404: HttpNotFoundError,
    405: HttpMethodNotAllowedError,
    429: HttpToManyRequestsError,
}


def create_http_error(http_code: int, raw_error: ErrorResponse) -> HttpError:
    """
    Create the correct HttpError for the http_code.

    Args:
        http_code (int): The http code to generate the error from
        raw_error (ErrorResponse): The raw error data from discord

    Returns:
        HttpError: The http error
    """
    return HTTP_ERRORS.get(http_code, HttpError)(http_code, raw_error)
