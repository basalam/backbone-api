from typing import List, Generic, TypeVar, Optional

from starlette.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT

from basalam.backbone_api.responses.client_error.base import Base400Response, Error
from basalam.backbone_api.responses.response_model_abstract import T


class ExtendedError(Error):
    fields: Optional[List[str]]


class ConflictResponse(Base400Response, Generic[T]):
    errors: List[ExtendedError]
    data: List[T]

    def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_409_CONFLICT
        )
