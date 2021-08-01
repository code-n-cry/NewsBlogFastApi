from fastapi import FastAPI, Request, Response, staticfiles, HTTPException
from app.routes import users, posts
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from databases import Database


app = FastAPI()
security = HTTPBasic()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")
app.include_router(users.router)
app.include_router(posts.router)
template_folder = Jinja2Templates('templates')
database = Database("db/news.sqlite")


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
    print(request)
    return template_folder.TemplateResponse("index.html", {"request": request, "title": "FandomIt!"})
