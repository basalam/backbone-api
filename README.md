# backbone-api
OpenAPI request and response models

#### Installation & Upgrade

```shell
pip install basalam.backbone-api
```

#### TODO List
- [ ] Add Message Toast Field
- [ ] Add Pagination Query Params Dependency

#### Usage Example

```python
import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel

from basalam.backbone_api.responses import (
    ForbiddenResponse,
    NotFoundResponse,
    UnauthorizedResponse,
    UnprocessableContentResponse,
    BulkResponse, ConflictResponse
)

app = FastAPI()


class User(BaseModel):
    id: int
    name: str


router = APIRouter(responses={
    401: {"model": UnauthorizedResponse},
    403: {"model": ForbiddenResponse},
    404: {"model": NotFoundResponse},
    409: {"model": ConflictResponse},
    422: {"model": UnprocessableContentResponse}
})


@router.get("/", response_model=BulkResponse[User])
async def root():
    ls = [
        User(id=1, name="John Doe"),
        User(id=2, name="Jane Boe")
    ]
    return BulkResponse(data=ls).as_json_response()

app.include_router(router)
if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)
```
### Using Exceptions
in app.py

```python
from fastapi import FastAPI
from basalam.backbone_api.exceptions.client_error.handlers import client_error_exception_handler
from basalam.backbone_api.exceptions.client_error import (
    ClientErrorException,
    ForbiddenException,
    UnauthorizedException,
    ConflictException,
    NotFoundException,
    UnprocessableEntityException
)

app = FastAPI()

exception_handlers = {
    ClientErrorException: client_error_exception_handler,
    ForbiddenException: client_error_exception_handler,
    UnauthorizedException: client_error_exception_handler,
    ConflictException: client_error_exception_handler,
    NotFoundException: client_error_exception_handler,
    UnprocessableEntityException: client_error_exception_handler,
}

...

```
If you raise any of these exceptions everywhere in you FastAPI project FastAPI will return a client error response
based on the excpetion.

### Example Usage

```python
def view_or_somthing_else():
    raise ForbiddenException()
```

### Application error codes

All client-error exception constructors accept the optional, keyword-only
`code` argument. It is returned as `errors[].code` so clients can distinguish
errors without matching message text. Existing calls default to `0`; HTTP
statuses and response structure are unchanged.

```python
raise ForbiddenException(message="Reason is not accessible", code=40304)
raise NotFoundException(code=40401)
raise UnprocessableEntityException(
    message="Campaign is required",
    fields=["campaign_id"],
    code=42203,
)
raise ConflictException(data=[{"id": 123}], code=40901)
```

Codes are chosen by the application, not assigned by this library.
`BadRequestException` (400), `PaymentRequiredException` (402), and
`TooManyRequestsException` (429) are also available from
`basalam.backbone_api.exceptions` and `basalam.backbone_api.exceptions.client_error`.
Each accepts optional `message`, `fields`, and keyword-only `code` arguments:

```python
from basalam.backbone_api.exceptions import BadRequestException, TooManyRequestsException

raise BadRequestException(message="Insufficient balance", fields=["amount"], code=40001)
raise TooManyRequestsException(code=42901)
```

Registering the same `client_error_exception_handler` handles these exceptions
with the correct HTTP status and preserves their error fields. The corresponding
`BadRequestResponse`, `PaymentRequiredResponse`, and `TooManyRequestsResponse`
models are exported from `basalam.backbone_api.responses` for OpenAPI declarations.

`UnauthorizedException` and the base `ClientErrorException` also accept `code`.
For `ClientErrorException(http_status=400, code=40001)`, the code is applied to
the default error detail. If an explicit `errors` list is supplied, its details
and individual codes are preserved instead:

```python
from basalam.backbone_api.exceptions.client_error import ClientErrorException, ErrorDetail

raise ClientErrorException(
    http_status=422,
    errors=[
        ErrorDetail(code=42210, message="Field is required", fields=["amount"]),
        ErrorDetail(code=42211, message="Invalid integer", fields=["user_id"]),
    ],
)
```

#### Credits
This project was inspired by the work of [Mr.MohammadAli Soltanipoor](https://github.com/soltanipoor) on OpenAPI. 
