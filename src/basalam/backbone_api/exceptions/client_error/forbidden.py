from api.exceptions.base import ErrorDetail, BadRequestException


class ForbiddenException(BadRequestException):
    def __init__(self, message: str = 'شما دسترسی لازم برای استفاده از این منبع را ندارید') -> None:
        errors = [
            ErrorDetail(
                code=0,
                message=message,
                fields=None,
                data=None
            )
        ]
        super().__init__(http_status=403, errors=errors)
