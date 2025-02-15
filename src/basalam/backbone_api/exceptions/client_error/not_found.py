from api.exceptions.base import ErrorDetail, BadRequestException


class NotFoundException(BadRequestException):
    def __init__(self, message: str = 'یافت نشد') -> None:
        errors = [
            ErrorDetail(
                code=0,
                message=message,
                fields=None,
                data=None
            )
        ]
        super().__init__(http_status=404, errors=errors)
