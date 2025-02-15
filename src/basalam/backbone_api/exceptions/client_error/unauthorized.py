from api.exceptions.base import ErrorDetail, BadRequestException


class UnauthorizedException(BadRequestException):
    def __init__(self, message: str = 'ابتدا وارد حساب کاربری خود شوید') -> None:
        errors = [
            ErrorDetail(
                code=0,
                message=message,
                fields=None,
                data=None
            )
        ]
        super().__init__(http_status=401, errors=errors)
