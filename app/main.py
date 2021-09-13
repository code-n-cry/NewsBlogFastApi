from logging import DEBUG
from fastapi.params import Form
from fastapi import FastAPI, Request, Response, staticfiles
from fastapi.param_functions import Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.sql.functions import current_user
from app.routers import user, posts
from app.config import database
from app.utils.posts import get_posts
from fastapi_jwt_auth.exceptions import AuthJWTException

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="app/static"), name="static")
app.include_router(user.router)
app.include_router(posts.router)
template_folder = Jinja2Templates('app/templates')


@app.on_event("startup")
async def on_startup():
    global database
    await database.connect()
    

@app.on_event("shutdown")
async def on_shutdown():
    global database
    await database.disconnect()


@app.get("/")
async def index(request: Request):
    all_posts = [dict(i) for i in await get_posts()]
    return template_folder.TemplateResponse("index.html", {"request": request, "title": "FandomIt!", "total_count": len(all_posts), "all_posts": all_posts})


@app.get('/unauthorized')
async def unauth(request: Request):
    return template_folder.TemplateResponse("401.html", {"request": request, "title": "Вы не авторизованы!"})


@app.get("/my_posts")
async def get_my_posts(request: Request):
    return template_folder.TemplateResponse("my_posts.html", {"request": request, "title": "FandomIt!: Мои посты"})


@app.get('/my_post/{post_id}')
async def get_my_post(post_id: int, request: Request):
    return template_folder.TemplateResponse("my_post.html", {"request": request, "title": f"FandomIt!: Пост №{post_id}"})


@app.get("/register")
async def register(request: Request):
    return template_folder.TemplateResponse("register.html", {"request": request, "title": "FandomIt!: Регистрация"})


@app.get("/login")
async def login(request: Request):
    return template_folder.TemplateResponse("login.html", {"request": request, "title": "FandomIt!: Вход"})


@app.get('/create')
async def create_post(request: Request):
    return template_folder.TemplateResponse("create.html", {"request": request, "title": "FandomIt!: Создать пост"})

@app.exception_handler(AuthJWTException)
async def authjwt_exception_handler(request: Request, error: AuthJWTException):
    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.message}
    )
    

@app.get('/profile')
async def profile(request: Request):
    return template_folder.TemplateResponse('profile.html', {'request': request, 'title': 'FandomIt!: Профиль'})


@app.get('/forbidden')
async def forbidden(request: Request):
    return template_folder.TemplateResponse('403.html', {'request': request, 'title': 'FandomIt!: Нельзя!'})