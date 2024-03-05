from fastapi import FastAPI, Request
import miniflux
# from app.api.movies import movies
from api.feeds import feeds
# from app.api.db import metadata, database, engine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import secrets
# load API key using dotenv
from dotenv import load_dotenv
import os
from dependencies import get_authenticated_client
import uvicorn
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

@app.get("/mini")
def root():
    try:
        client = miniflux.Client("http://localhost", api_key="xEzgfo_f3_E8kCwW3cPMdX6HIEV59AXIN8xeF8BB83U=")
    except Exception as e:
        raise HTTPException("Error:" + e)
    try:
        feeds = client.me()
    except Exception as e:
        print(e)
        return
    return (feeds)

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)

# app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
app.include_router(feeds, prefix='/api/v1/feeds', tags=['feeds'])

