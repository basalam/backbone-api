from typing import List

from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from basalam.backbone_api.responses.response_model_abstract import ResponseModelAbstract


class Error(BaseModel):
    code: int | None = 0
    message: str | None = None


class Base400Response(ResponseModelAbstract):
    http_status: int = 400
    message: str
    errors: List[Error] | None

    def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_400_BAD_REQUEST
        )
