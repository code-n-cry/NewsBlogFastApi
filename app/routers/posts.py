from app.schemas.posts import PostDetailsBase, PostBase
from app.data import user, post
from app.config import database
from app.utils import posts as post_utils
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
import hashlib
from sqlalchemy import select
import base64

router = APIRouter()


@router.post("/posts", response_model=PostDetailsBase, status_code=201)
async def create_post(post: PostBase, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    current_user_info = await database.fetch_one(select([user.table_of_users.c.id, user.table_of_users.c.nickname])
                                                 .select_from(user.table_of_users).where(user.table_of_users.c.email == current_user_email))
    if not post.image is None:
        for file in post.image:
            image_hash_name = hashlib.sha256((current_user_email + file['filename']).encode('utf-8')).hexdigest() + '.jpg'
            with open('app/static/img/' + image_hash_name, mode='wb') as new_img:
                new_img.write(base64.b64decode(file['data']))
        post.images = '/img/' + image_hash_name
    post = await post_utils.create_post(post, dict(current_user_info))
    return post


@router.get("/posts")
async def get_posts():
    total_cout = await post_utils.get_posts_count()
    posts = await post_utils.get_posts()
    return {"total_count": total_cout, "results": posts}


@router.get("/posts/{post_id}", response_model=PostDetailsBase)
async def get_post(post_id: int):
    return await post_utils.get_post(post_id)

@router.get("/posts/me")
async def my_posts(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    query = select([user.table_of_users.c.id]).select_from(user.table_of_users).where(user.table_of_users.c.email == current_user_email)
    user_id = await database.fetch_one(query)
    users_posts = await post_utils.get_my_posts(dict(user_id)['id'])
    return {'total_count': len(users_posts), 'results': users_posts}



@router.put("/posts/{post_id}", response_model=PostDetailsBase)
async def update_post(post_id: int, post_data: PostBase, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    query = select([user.table_of_users.c.id]).select_from(user.table_of_users).where(user.table_of_users.c.email == current_user_email)
    current_user_id = await database.fetch_one(query)
    post = await post_utils.get_post(post_id)
    if post["user_id"] != dict(current_user_id)["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this post",
        )
    if post_data.image:
        image_hash_name =  '/img/' + hashlib.sha256((current_user_email + post_data.image[0]['filename']).encode('utf-8')).hexdigest() + '.jpg'
        if dict(post)['image']:
            print(image_hash_name)
            image_hash_name = dict(post)['image']
            for file in post_data.image:
                with open(f'app/static{image_hash_name}', mode='wb') as new_img:
                    new_img.write(base64.b64decode(file['data']))
        post_data.image = image_hash_name
    await post_utils.update_post(post_id=post_id, post=post_data)
    return await post_utils.get_post(post_id)


@router.delete('/posts/{post_id}')
async def delete_post(post_id: int, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    query = select([user.table_of_users.c.id]).select_from(user.table_of_users).where(user.table_of_users.c.email == current_user_email)
    current_user_id = await database.fetch_one(query)
    print(await post_utils.get_posts_author(current_user_id, post_id))
    if await post_utils.get_posts_author(dict(current_user_id)['id'], post_id):
        await post_utils.delete_post(post_id)
        return {'200': 'OK'}
    raise HTTPException(status_code=403, detail="You don't have access to delete this post")


@router.get('/posts/{post_id}/author')
async def get_post_author(post_id: int, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    query = select([user.table_of_users.c.id]).select_from(user.table_of_users).where(user.table_of_users.c.email == current_user_email)
    current_user_id = await database.fetch_one(query)
    is_user_author = await post_utils.get_posts_author(dict(current_user_id)['id'], post_id)
    if is_user_author:
        return {'200': 'OK'}
    elif is_user_author is None:
        raise HTTPException(404, detail="Post doesn't exist")
    raise HTTPException(403, detail="You aren't after of this post!")
    