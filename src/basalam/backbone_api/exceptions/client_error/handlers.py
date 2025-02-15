from starlette.requests import Request

from basalam.backbone_api.exceptions.client_error.base import ClientErrorException, ClientErrorExceptionMapper


async def client_error_exception_handler(request: Request, exception: ClientErrorException):
    """
    Handles client error exceptions and maps them to a JSON response.

    Parameters:
        request: The incoming HTTP request.
        exception: The raised `ClientErrorException`.

    Returns:
        JSONResponse: A structured JSON response with error details.
    """
    return await (ClientErrorExceptionMapper(request=request, exception=exception)).map()
