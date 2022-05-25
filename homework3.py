import datetime

from fastapi import FastAPI, HTTPException, status, Depends, Query, Header
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def how_old(date):
    today = datetime.date.today()
    return today.year - date.year - ((today.month, today.day) < (date.month, date.day))


app = FastAPI()

security = HTTPBasic()


@app.get('/start', response_class=HTMLResponse)
def start():
    return '<h1>The unix epoch started at 1970-01-01</h1>'


@app.post('/check', response_class=HTMLResponse)
def check(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    try:
        birthday = datetime.date.fromisoformat(password)
    except ValueError as e:
        print("ERROR:", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    age = how_old(birthday)
    if age <= 16:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return f'<h1>Welcome {username}! You are {age}</h1>'


@app.get('/info')
def info(format: str | None = Query(None), user_agent: str | None = Header(default=None)):
    print(format)
    print(user_agent)
    match format:
        case 'json':
            json_content = {"user_agent": user_agent}
            return JSONResponse(content=json_content, status_code=200)
        case 'html':
            html_content = f'<input type="text" id=user-agent name=agent value="{user_agent}">'
            return HTMLResponse(content=html_content, status_code=200)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
