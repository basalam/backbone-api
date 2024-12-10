from typing import Generic, List, Annotated, Union

from fastapi import Depends
from starlette.responses import JSONResponse

from basalam.backbone_api.responses.response_model_abstract import ResponseModelAbstract, T


class OffsetPaginationResponse(ResponseModelAbstract, Generic[T]):
    data: List[T]
    total_count: int
    total_page: int
    page: int
    result_count: int
    per_page: int

    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(content=self.model_dump(), status_code=200)


class OffsetPaginationQueryParams:
    def __init__(self, page: Union[int, None] = None, per_page: Union[int, None] = None):
        self.page = page
        self.per_page = per_page


OffsetPaginationQueryParamsDepend = Annotated[OffsetPaginationQueryParams, Depends(OffsetPaginationQueryParams)]
