"""
This package provides custom exception handling for client errors.

It includes different types of client error exceptions, a structure for
handling error details, and a handler for mapping these exceptions to
HTTP responses.

Modules:
    - base: Contains base classes for error handling.
    - conflict: Defines conflict-related error exceptions.
    - forbidden: Defines forbidden-related error exceptions.
    - not_found: Defines not found-related error exceptions.
    - unauthorized: Defines unauthorized error exceptions.
    - unprocessable_entity: Defines unprocessable error exceptions.
"""

from basalam.backbone_api.exceptions.client_error.conflict import ConflictException
from basalam.backbone_api.exceptions.client_error.forbidden import ForbiddenException
from basalam.backbone_api.exceptions.client_error.not_found import NotFoundException
from basalam.backbone_api.exceptions.client_error.unauthorized import UnauthorizedException
from basalam.backbone_api.exceptions.client_error.unprocessable_entity import UnprocessableEntityException
from basalam.backbone_api.exceptions.client_error.base import ClientErrorException, ErrorDetail, Error
