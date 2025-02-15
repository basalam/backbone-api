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
"""

from basalam.backbone_api.exceptions.conflict import ConflictException
from basalam.backbone_api.exceptions.forbidden import ForbiddenException
from basalam.backbone_api.exceptions.not_found import NotFoundException
from basalam.backbone_api.exceptions.unauthorized import UnauthorizedException
from basalam.backbone_api.exceptions.base import BadRequestException, ErrorDetail, Error
