from abc import ABC, abstractmethod
from typing import TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class ResponseModelAbstract(BaseModel, ABC):

    @abstractmethod
    async def as_json_response(self) -> JSONResponse:
        raise NotImplementedError
