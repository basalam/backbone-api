from typing import List

from pydantic import BaseModel
from starlette.responses import JSONResponse

from basalam.backbone_api.responses.response_model_abstract import ResponseModelAbstract


class Error(BaseModel):
    code: int | None = 0
    message: str


class Base400Response(ResponseModelAbstract):
    http_status: int
    message: str
    errors: List[Error] | None

    async def as_json_response(self) -> JSONResponse:
        pass
