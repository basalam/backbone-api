from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

from basalam.backbone_api.responses.client_error.base import Base400Response


class NotFoundResponse(Base400Response):
    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_404_NOT_FOUND
        )
