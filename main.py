from fastapi import FastAPI, Request, Response, staticfiles, HTTPException
from fastapi.params import Depends
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import select
from app.routes import users, posts
from app.utils import dependecies
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from app.config import database
import requests


app = FastAPI()
security = HTTPBasic()
app.mount("/static", staticfiles.StaticFiles(directory="app/static"), name="static")
app.include_router(users.router)
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
    all_posts = await posts.get_posts()
    print(all_posts)
    return template_folder.TemplateResponse("index.html", {"request": request, "title": "FandomIt!"})


@app.get("/my_posts")
async def get_my_posts(request: Request):
    return template_folder.TemplateResponse("my_posts.html", {"request": request, "title": "FandomIt!: Мои посты"})


@app.get("/register")
async def register(request: Request):
    return template_folder.TemplateResponse("register.html", {"request": request, "title": "FandomIt!: Регистрация"})