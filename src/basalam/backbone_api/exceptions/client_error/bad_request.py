from typing import List, Optional

from basalam.backbone_api.exceptions.client_error.base import ClientErrorException, ErrorDetail


class BadRequestException(ClientErrorException):
    def __init__(self, message: Optional[str] = None, fields: Optional[List[str]] = None, *, code: int = 0) -> None:
        super().__init__(
            http_status=400,
            errors=[ErrorDetail(code=code, message=message, fields=fields)],
        )
