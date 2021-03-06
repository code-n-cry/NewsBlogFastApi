from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import user
from app.config import database
from app.data.post import table_of_posts
from app.data.user import table_of_users
from app.schemas import posts
from sqlalchemy import desc, func, select


async def create_post(post: posts.PostBase, user):
    query = (
        table_of_posts.insert().values(
            title=post.title,
            content=post.content,
            image=post.image,
            creation_date=datetime.now(),
            user_id=user["id"]
        ).returning(
            table_of_posts.c.id,
            table_of_posts.c.title,
            table_of_posts.c.content,
            table_of_posts.c.user_id,
            table_of_posts.c.creation_date
        )
    )
    post = await database.fetch_one(query)
    post = dict(zip(post, post.values()))
    post["nickname"] = user["nickname"]
    return post


async def get_post(id):
    query = (
        select(
            [
                table_of_posts.c.id,
                table_of_posts.c.title,
                table_of_posts.c.content,
                table_of_posts.c.image,
                table_of_posts.c.creation_date,
                table_of_posts.c.user_id,
                table_of_users.c.nickname
            ]
        ).select_from(table_of_posts.join(table_of_users)).where(table_of_posts.c.id == id)
    )
    post = await database.fetch_one(query)
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def get_posts_count():
    query = select([func.count()]).select_from(table_of_posts)
    return await database.fetch_val(query)


async def update_post(post_id: int, post: posts.PostBase):
    query = (
        table_of_posts.update()
        .where(table_of_posts.c.id == post_id)
        .values(title=post.title, content=post.content)
    )
    return await database.execute(query)


async def get_my_posts(user_id):
    query = select(
        [table_of_posts.c.id, table_of_posts.c.title, table_of_posts.c.content, table_of_posts.c.image, table_of_posts.c.creation_date]).select_from(table_of_posts).where(
        table_of_posts.c.user_id == user_id
    )
    users_posts = [dict(i) for i in await database.fetch_all(query)]
    return users_posts


async def delete_post(post_id):
    query = table_of_posts.delete().where(table_of_posts.c.id == post_id)
    deleted = await database.execute(query)
    return deleted


async def get_posts():
    query = select([
        table_of_posts.c.id,
        table_of_posts.c.title,
        table_of_posts.c.content,
        table_of_posts.c.image,
        table_of_posts.c.creation_date,
        table_of_posts.c.user_id,
        table_of_users.c.nickname
    ]).select_from(table_of_posts.join(table_of_users)).order_by(desc(table_of_posts.c.creation_date))
    return await database.fetch_all(query)


async def get_posts_author(user_id, post_id):
    query = select([table_of_posts.c.user_id]).select_from(
        table_of_posts).where(table_of_posts.c.id == post_id)
    post_author = await database.fetch_one(query)
    if not isinstance(post_author, None):
        return user_id == dict(post_author)['user_id']
    return None
