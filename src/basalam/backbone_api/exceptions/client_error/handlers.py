from typing import Type

from starlette.requests import Request

from basalam.backbone_api.exceptions.client_error.conflict import ConflictException
from basalam.backbone_api.exceptions.client_error.forbidden import ForbiddenException
from basalam.backbone_api.exceptions.client_error.not_found import NotFoundException
from basalam.backbone_api.exceptions.client_error.unauthorized import UnauthorizedException
from basalam.backbone_api.exceptions.client_error.unprocessable_entity import UnprocessableEntityException
from basalam.backbone_api.exceptions.client_error.base import ClientErrorException
from basalam.backbone_api.responses.client_error.base import Base400Response, Error as ClientError
from basalam.backbone_api.responses.client_error.conflict import ConflictResponse, \
    ExtendedError as ConflictExtendedError
from basalam.backbone_api.responses.client_error.not_found import NotFoundResponse
from basalam.backbone_api.responses.client_error.unprocessable_content import UnprocessableContentResponse, \
    ExtendedError as UnprocessableContentExtendedError
from basalam.backbone_api.responses.client_error.unauthorized import UnauthorizedResponse
from basalam.backbone_api.responses.client_error.forbidden import ForbiddenResponse


# Helper function to map exception to response
def map_exception_to_response(exception: ClientErrorException, response_class: Type[Base400Response],
                              error_class: Type[ClientError], is_conflict: bool = False):
    """
    Maps the exception data to a response.
    """
    response_data = exception.response_data
    errors = [error_class(message=data.message, code=data.code, fields=data.fields) for data in response_data]
    if is_conflict:
        return response_class(message=exception.message, errors=errors, data=response_data[0].data, http_status=exception.http_status).as_json_response()
    return response_class(message=exception.message, errors=errors, http_status=exception.http_status).as_json_response()


def client_error_exception_handler(request: Request, exception: ClientErrorException):
    """
    Handles client error exceptions and maps them to a JSON response.

    Parameters:
        request: The incoming HTTP request.
        exception: The raised `ClientErrorException`.

    Returns:
        JSONResponse: A structured JSON response with error details.
    """
    if isinstance(exception, UnprocessableEntityException):
        return map_exception_to_response(exception, UnprocessableContentResponse, UnprocessableContentExtendedError)
    elif isinstance(exception, ConflictException):
        return map_exception_to_response(exception, ConflictResponse, ConflictExtendedError, is_conflict=True)
    elif isinstance(exception, NotFoundException):
        return map_exception_to_response(exception, NotFoundResponse, ClientError)
    elif isinstance(exception, ForbiddenException):
        return map_exception_to_response(exception, ForbiddenResponse, ClientError)
    elif isinstance(exception, UnauthorizedException):
        return map_exception_to_response(exception, UnauthorizedResponse, ClientError)
    else:
        return map_exception_to_response(exception, Base400Response, ClientError)
