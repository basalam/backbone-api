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
#### Credits
This project was inspired by the work of [Mr.MohammadAli Soltanipoor](https://github.com/soltanipoor) on OpenAPI. 
