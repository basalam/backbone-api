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
    return await BulkResponse(data=ls).as_json_response()

app.include_router(router)
if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)
```
#### Credits
This project was inspired by the work of [Mr.MohammadAli Soltanipoor](https://github.com/soltanipoor) on OpenAPI. 