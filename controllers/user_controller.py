from fastapi import APIRouter
from passlib.context import CryptContext

import models
from dtos.user import AddNewUserReq, AddNewUserRes

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)


@router.get('/')
async def get_all_users(db: models.Db):
    query = db.query(models.User)
    print(str(query))
    users = query.all()

    return {'users': users}


"""

firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    role = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)

"""


@router.post('/', response_model=AddNewUserRes)
# should be in a service
async def add_new_user(req: AddNewUserReq, db: models.Db):
    new_user = models.User(lastName=req.lastName, firstName=req.firstName, email=req.username, role=req.role,
                           password=bcrypt_context.hash(req.password))

    db.add(new_user)
    db.commit()

    return new_user


"""

"user": {
    {
  "username": "string",
  "id": 0,
  "firstName": "string",
  "lastName": "string",
  "role": "string"
}

"""
