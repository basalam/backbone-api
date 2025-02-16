from typing import Optional, List, Dict

from basalam.backbone_api.exceptions.client_error.base import ClientErrorException, ErrorDetail


class ConflictException(ClientErrorException):
    def __init__(self, data: Optional[List[Dict]], message: str = None):
        errors = [
            ErrorDetail(
                data=data,
                message=message,
            )
        ]
        super().__init__(http_status=409, errors=errors)
