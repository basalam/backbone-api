from typing import Generic, List

from starlette.responses import JSONResponse

from basalam.backbone_api.responses.response_model_abstract import ResponseModelAbstract, T


class BulkResponse(ResponseModelAbstract, Generic[T]):
    data: List[T]

    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(content=self.model_dump(), status_code=200)
