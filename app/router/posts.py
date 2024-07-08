
from fastapi import Depends, HTTPException, Response, status,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hash
from  .. import schema,models,oauth2
from typing import List,Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
@router.get("/",response_model=List[schema.PostVote])
def get_posts(db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit:int=10, skip:int =0, search:Optional[str]=""):

    # by default is a inner inner join
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post :schema.PostCreate,db:Session = Depends(get_db),current_user :int=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==current_user.id)
    if user :

        new_post = models.Post(**post.dict(),user_id=current_user.id) 
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id {user.id} was not found")



@router.get('/{id}',response_model=schema.PostVote)
def get_post(id:int, db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    else:
        return post
    
@router.delete('/{id}')
def delete_posts(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.user_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")
    db.delete(post)  
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    
@router.put('/{id}',response_model=schema.Post)
def update_posts(id:int,post_data:schema.Post,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.user_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")
    post_query.update(post_data.dict(),user_id = current_user.id,synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
    