from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

from basalam.backbone_api.responses.client_error.base import Base400Response


class ForbiddenResponse(Base400Response):
    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_403_FORBIDDEN
        )
