from typing import Optional, List, Dict

from api.exceptions.base import BadRequestException, ErrorDetail


class ConflictException(BadRequestException):
    def __init__(self, data=Optional[List[Dict]]):
        errors = [
            ErrorDetail(
                data=data
            )
        ]
        super().__init__(http_status=409, errors=errors)
