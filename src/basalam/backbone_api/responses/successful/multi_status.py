from typing import Generic, List

from pydantic import BaseModel
from starlette.responses import JSONResponse

from basalam.backbone_api.responses.response_model_abstract import ResponseModelAbstract, T


class Error(BaseModel):
    code: int | None = 0
    message: str
    fields: List[str]


class Failure:
    path: str
    http_status: int
    errors: List[Error]


class MultiStatusResponse(ResponseModelAbstract, Generic[T]):
    data: List[T]
    failures: List[Failure]
    success_count: int
    failure_count: int

    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(content=self.model_dump(), status_code=200)
