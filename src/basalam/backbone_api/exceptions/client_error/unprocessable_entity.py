from typing import List, Optional, Tuple

from basalam.backbone_api.exceptions.client_error.base import ClientErrorException, ErrorDetail


class UnprocessableEntityException(ClientErrorException):
    def __init__(self, message: str, fields: Optional[List[str]] = None) -> None:
        errors = [
            ErrorDetail(
                message=message,
                fields=fields,
            )
        ]
        super().__init__(http_status=404, errors=errors)
