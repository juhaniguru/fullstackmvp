from pydantic import BaseModel


class AddNewLocationReq(BaseModel):
    name: str
    address: str
    zip_code: str


class AddNewLocationRes(AddNewLocationReq):
    id: int
