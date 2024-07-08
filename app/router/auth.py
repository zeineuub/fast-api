from fastapi import  APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schema,models, utils,oauth2
router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schema.Token)
def login(user_credentials:schema.UserLogin,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    # verify the password with hashed one
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    # create token
    # return the token
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return  { "access_token":access_token,"token_type":"bearer"}