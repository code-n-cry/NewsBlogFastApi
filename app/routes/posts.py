from app.schemas.posts import PostDetailsBase, PostBase
from app.schemas.users import User
from app.data import user, post
from app.config import database
from app.utils import posts as post_utils
from app.utils.dependecies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/posts", response_model=PostDetailsBase, status_code=201)
async def create_post(post: PostBase, current_user: User = Depends(get_current_user)):
    post = await post_utils.create_post(post, current_user)
    return post


@router.get("/posts")
async def get_posts(page: int = 1):
    total_cout = await post_utils.get_posts_count()
    posts = await post_utils.get_posts()
    return {"total_count": total_cout, "results": posts}


@router.get("/posts/{post_id}", response_model=PostDetailsBase)
async def get_post(post_id: int):
    return await post_utils.get_post(post_id)

@router.get("/posts/me")
async def my_posts(user: User = Depends(get_current_user)):
    query = post.table_of_posts.select(
        [post.table_of_posts.c.title, post.table_of_posts.c.content, post.table_of_posts.c.creation_date]).where(
        post.table_of_posts.c.user_id == user.id
    )
    return database.fetch_all(query)



@router.put("/posts/{post_id}", response_model=PostDetailsBase)
async def update_post(
    post_id: int, post_data: PostBase, current_user=Depends(get_current_user)
):
    post = await post_utils.get_post(post_id)
    if post["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this post",
        )

    await post_utils.update_post(post_id=post_id, post=post_data)
    return await post_utils.get_post(post_id)
