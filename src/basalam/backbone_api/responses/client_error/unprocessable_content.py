from typing import List

from starlette.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT

from basalam.backbone_api.responses.client_error.base import Base400Response, Error


class ExtendedError(Error):
    fields: List[str]


class UnprocessableContentResponse(Base400Response):
    errors: List[ExtendedError]

    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_409_CONFLICT
        )
