from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from basalam.backbone_api.responses.client_error.base import Base400Response


class UnauthorizedResponse(Base400Response):
    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_401_UNAUTHORIZED
        )
