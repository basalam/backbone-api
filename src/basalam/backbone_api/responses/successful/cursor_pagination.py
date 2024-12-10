import base64
import json
from typing import Generic, Optional, Dict, List, Annotated, Union

from fastapi import Depends
from pydantic import Field, field_validator
from starlette.responses import JSONResponse

from basalam.backbone_api.responses.response_model_abstract import ResponseModelAbstract, T


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

    @field_validator('next_cursor', mode='before')
    def check_cursor(cls, values):
        cursor = values.get('next_cursor')
        if cursor:
            values['next_cursor'] = Cursor.decode_cursor(cursor)
        return values

    async def as_json_response(self) -> JSONResponse:
        return JSONResponse(content=self.model_dump(), status_code=200)


class CursorPaginationQueryParams:
    def __init__(self, cursor: Union[str, None] = None):
        self.cursor = Cursor.decode_cursor(cursor)


CursorPaginationQueryParamsDepend = Annotated[CursorPaginationQueryParams, Depends(CursorPaginationQueryParams)]
