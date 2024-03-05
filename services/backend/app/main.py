import logging
import sys
from contextlib import asynccontextmanager
from app.api.dependencies.core import DBSessionDep
import uvicorn
from app.api.routers.users import router as users_router
from app.config import settings
from app.database import sessionmanager
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from app.schemas.auth import Token
from app.utils.auth import create_access_token, authenticate_user
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug_logs else logging.INFO)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: DBSessionDep,
) -> Token:
    user = await authenticate_user( db_session ,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Routers
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
