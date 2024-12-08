from abc import ABC, abstractmethod
from typing import Dict, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModelAbstract(BaseModel, ABC, ):

    @classmethod
    @abstractmethod
    async def resource(cls, **kwargs) -> Dict:
        pass
