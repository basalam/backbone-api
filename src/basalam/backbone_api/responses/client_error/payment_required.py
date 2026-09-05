from typing import List

from starlette.responses import JSONResponse
from starlette.status import HTTP_402_PAYMENT_REQUIRED

from basalam.backbone_api.responses.client_error.base import Base400Response, DetailedError


class PaymentRequiredResponse(Base400Response):
    http_status: int = 402
    errors: List[DetailedError] | None

    def as_json_response(self) -> JSONResponse:
        return JSONResponse(content=self.model_dump(), status_code=HTTP_402_PAYMENT_REQUIRED)
