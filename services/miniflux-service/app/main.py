from fastapi import FastAPI, Request
import miniflux
# from app.api.movies import movies
from app.api.feeds import feeds
# from app.api.db import metadata, database, engine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import secrets
# load API key using dotenv
from dotenv import load_dotenv
import os
from .dependencies import get_authenticated_client
# metadata.create_all(engine)
load_dotenv()
app = FastAPI()

security = HTTPBasic()

URL = os.getenv("MINIFLUX_URL")




# Then, use this dependency in your routes
@app.get("/users/me")
def read_current_user(request: Request, client: miniflux.Client = Depends(get_authenticated_client)):
    request.app.state.miniflux_client = client
    return {"username": client.me()['username']}

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
app.include_router(feeds, prefix='/api/v1/feeds', tags=['feeds'])

