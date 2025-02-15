from http import HTTPStatus
from typing import List, Dict, Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request

"""
This module defines the base error handling for client errors, including
the structure of error details, and a custom HTTP exception class for
client errors.

Classes:
    - ErrorDetail: Structure for error details.
    - Error: Structure for the full error response.
    - ClientErrorException: Custom exception for client errors.
    - ClientErrorExceptionMapper: Maps client errors to JSON responses.
"""


class ErrorDetail(BaseModel):
    """
    Represents detailed information about a specific error.

    Attributes:
        code: A numerical code associated with the error.
        message: A description of the error.
        fields: Optional fields associated with the error.
        data: Optional additional data related to the error.
    """

    code: Optional[int] = 0
    message: Optional[str] = None
    fields: Optional[List[str]] = None
    data: Optional[List[Dict]] = None


class Error(BaseModel):
    http_status: int
    message: str
    errors: List[ErrorDetail]


class ClientErrorException(HTTPException):
    """
    Custom exception for client errors.

    This class is used to raise HTTP exceptions with detailed error
    information in the response.

    Attributes:
        http_status: HTTP status code of the error (e.g., 400, 404).
        errors: A list of `ErrorDetail` objects providing specifics
                about the error.

    Methods:
        to_response: Converts the exception to a JSON response.
    """

    def __init__(self, http_status: int, errors: List[ErrorDetail]) -> None:
        self.http_status = http_status
        self.errors = errors
        super().__init__(status_code=http_status, detail=self.message)

    @property
    def message(self) -> str:
        return HTTPStatus(self.http_status).phrase

    def to_response(self) -> JSONResponse:
        error = Error(
            http_status=self.http_status,
            message=self.message,
            errors=self.errors
        )

        return JSONResponse(
            status_code=self.http_status,
            content=error.dict()
        )


class ClientErrorExceptionMapper:
    def __init__(self, request: Request, exception: ClientErrorException) -> None:
        self.__request = request
        self.__exception = exception

    async def map(self) -> JSONResponse:
        return self.__exception.to_response()
