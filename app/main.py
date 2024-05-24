# main.py
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
# directory imports
from .schema import schema
from .db import database,models
from .routes import user, todo ,authh
# google login
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["/index.html"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="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")


oauth = OAuth()
oauth.register(
    name='google',
    client_id="581598162325-1dlpgvdacikg9ahonknqt4m6tfo9vr48.apps.googleusercontent.com",
    client_secret="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",
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri="http://localhost:8000/auth",
    client_kwargs={'scope': 'openid profile email'},
)

@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = await oauth.google.parse_id_token(request, token)
        email = user.get('email')
        name = user.get('name')
        # Handle user authentication and session creation here
        return JSONResponse(content={'user': user})
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=str(error))
    


@app.get("/")
async def read_index():
    return RedirectResponse(url="/index.html")


app.include_router(authh.router)
app.include_router(user.router)
app.include_router(todo.router)
