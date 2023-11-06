from fastapi import APIRouter

import models
from dtos.location import AddNewLocationReq, AddNewLocationRes

router = APIRouter(
    prefix='/api/v1/locations',
    tags=['locations']
)

"""

name: "sdlkjfsdlkdsfjsdfl",
"address": "ldskjfdlsdfkjfsdlkfsd",
"zip_code": "sdlkfdjsdlfkfjdsl"

"""


@router.post('/', response_model=AddNewLocationRes)
# should be in a service
async def add_new_location(req: AddNewLocationReq, db: models.Db):
    location = models.Location(**req.model_dump())
    # location = models.Location(name=req.name, address=req.address, zip_code=req.zip_code)

    db.add(location)
    db.commit()

    return location
