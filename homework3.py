import datetime

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
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
