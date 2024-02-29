from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import miniflux
from typing import Annotated
import os

from dotenv import load_dotenv
import os
# metadata.create_all(engine)
load_dotenv()

security = HTTPBasic()

URL = os.getenv("MINIFLUX_URL")

def get_authenticated_client(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> miniflux.Client:
    try:
        # Initialize the Miniflux client with the provided credentials
        client = miniflux.Client(URL, credentials.username.encode("utf8"), credentials.password.encode("utf8"))
        # Perform an action to validate the credentials, e.g., fetching the user's details
        user_info = client.me()
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to authenticate with provided credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return client
    except Exception as e:
        # Handle specific exceptions related to Miniflux authentication failure
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
