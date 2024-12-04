import base64
import json
from typing import Generic, TypeVar, Optional, Dict, List, Annotated, Union

from fastapi import Depends
from pydantic import Field

from .response_model_abstract import ResponseModelAbstract

T = TypeVar("T")


class Cursor:
    @staticmethod
    def encode_cursor(value: Dict = None) -> Union[str, None]:
        if not value:
            return None

        cursor_str = json.dumps(value, default=str)
        cursor_bytes = cursor_str.encode('utf-8')
        cursor_base64 = base64.urlsafe_b64encode(cursor_bytes)
        return cursor_base64.decode('utf-8')

    @staticmethod
    def decode_cursor(value: str = None) -> dict:
        if not value:
            return dict()

        try:
            cursor_bytes = base64.urlsafe_b64decode(value.encode('utf-8'))
            cursor_str = cursor_bytes.decode('utf-8')
            cursor = json.loads(cursor_str)
            return cursor if isinstance(cursor, dict) else dict()
        except ValueError:
            return dict()


class CursorPaginationResponse(ResponseModelAbstract, Generic[T]):
    data: List[T]
    next_cursor: Optional[str] = Field(None, json_schema_extra={"format": "base64"})

    @classmethod
    async def resource(cls, data: List[T], next_cursor: Dict = None) -> Dict:
        return dict(
            data=data,
            next_cursor=cls.encode_cursor(next_cursor),
        )


class CursorPaginationQueryParams:
    def __init__(self, cursor: Union[str, None] = None):
        self.cursor = Cursor.decode_cursor(cursor)


CursorPaginationQueryParamsDepend = Annotated[CursorPaginationQueryParams, Depends(CursorPaginationQueryParams)]
