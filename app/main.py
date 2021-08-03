from fastapi import FastAPI, Request, Response, staticfiles
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic
from fastapi.templating import Jinja2Templates
from app.config import database
from passlib.context import CryptContext
import importlib
asd = importlib.import_module("app.routers.user")
#from app.routers import users, posts
import os

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(os.listdir("app/routers"))
app.mount("/static", staticfiles.StaticFiles(directory="app/static"), name="static")
app.include_router(asd.user.router)
app.include_router(asd.routersposts.router)
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
    return template_folder.TemplateResponse("index.html", {"request": request, "title": "FandomIt!"})


@app.get("/my_posts")
async def get_my_posts(request: Request):
    print(request.headers)
    return template_folder.TemplateResponse("my_posts.html", {"request": request, "title": "FandomIt!: Мои посты"})


@app.get("/register")
async def register(request: Request):
    return template_folder.TemplateResponse("register.html", {"request": request, "title": "FandomIt!: Регистрация"})
