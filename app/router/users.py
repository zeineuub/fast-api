from fastapi import Depends, HTTPException, status,APIRouter,Response
from .. import models,schema,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hash
from typing import List


router = APIRouter(
    prefix='/users',
    tags=['Users']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate,db:Session = Depends(get_db)):
    # hash the password
    print(user)
    user.password=hash(user.password)
    new_user = models.User(**user.dict()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}")
def get_user(id: int,db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id ==id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with id {id} not found")
    
    return user

@router.delete('/{id}')
def delete_posts(id:int,db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"user with id {id} was not found")

    db.delete(user)  
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    
@router.put('/{id}',response_model=schema.UserOut)
def update_posts(id:int,user_data:schema.UserCreate,db:Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id==id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"user with id {id} was not found")
    
    user_query.update(user_data.dict(),synchronize_session=False)
    db.commit()
    return {"data": user_query.first()}
    