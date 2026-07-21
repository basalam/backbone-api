from typing import List

from starlette.responses import JSONResponse
try:
    # Starlette >= 0.47 renamed this constant; the old name is deprecated.
    from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT
except ImportError:  # pragma: no cover - older Starlette
    from starlette.status import (
        HTTP_422_UNPROCESSABLE_ENTITY as HTTP_422_UNPROCESSABLE_CONTENT,
    )

from basalam.backbone_api.responses.client_error.base import Base400Response, Error


class ExtendedError(Error):
    fields: Optional[List[str]]


class UnprocessableContentResponse(Base400Response):
    errors: List[ExtendedError]

    def as_json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=HTTP_422_UNPROCESSABLE_CONTENT
        )
