from abc import ABC, abstractmethod
from typing import Dict

from pydantic import BaseModel


class ResponseModelAbstract(BaseModel, ABC):

    @classmethod
    @abstractmethod
    async def resource(cls, **kwargs) -> Dict:
        pass
