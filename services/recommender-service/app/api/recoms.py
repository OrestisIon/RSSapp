from fastapi import APIRouter, HTTPException
from typing import List

from app.api import db_manager

recoms = APIRouter()

# Define the API endpoints
@recoms.get('/', response_model=CastOut, status_code=201)



@casts.get('/{id}/', response_model=CastOut)
async def get_cast(id: int):
    cast = await db_manager.get_cast(id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast