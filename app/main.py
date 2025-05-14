

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# 간단한 메모리 기반 사용자 저장소 (나중에 DB로 대체 가능)
fake_users = {}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def show_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if username in fake_users:
        return {"error": "이미 존재하는 사용자입니다."}
    fake_users[username] = bcrypt.hash(password)
    return RedirectResponse("/", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user_pw = fake_users.get(username)
    if user_pw and bcrypt.verify(password, user_pw):
        return {"message": f"{username}님 환영합니다!"}
    return {"error": "아이디 또는 비밀번호가 잘못되었습니다."}