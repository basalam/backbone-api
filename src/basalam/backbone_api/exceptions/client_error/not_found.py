from typing import Optional

from basalam.backbone_api.exceptions.client_error.base import ClientErrorException, ErrorDetail


class NotFoundException(ClientErrorException):
    def __init__(self, message: str = None, *, code: int = 0) -> None:
        if message:
            errors = [ErrorDetail(message=message, code=code)]
        else:
            errors = None
        super().__init__(http_status=404, errors=errors, code=code)
