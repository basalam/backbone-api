from typing import List

from basalam.backbone_api.responses.client_error.base import Base400Response, DetailedError


class BadRequestResponse(Base400Response):
    http_status: int = 400
    errors: List[DetailedError] | None
