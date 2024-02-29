from fastapi import FastAPI
from app.api.recom import recoms
from app.api.db import metadata, database, engine
from openai import OpenAI
from qdrant_client import QdrantClient
# load API key using dotenv
from dotenv import load_dotenv
import os
import time
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
qdrant_host = os.getenv("QDRANT_HOST")
qdrant_port = os.getenv("QDRANT_PORT")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

while api_key is None or qdrant_host is None or qdrant_port is None or qdrant_api_key is None:
    print("Waiting for environment variables to be loaded...")
    time.sleep(3)
    api_key = os.getenv("OPENAI_API_KEY")
    qdrant_host = os.getenv("QDRANT_HOST")
    qdrant_port = os.getenv("QDRANT_PORT")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    

print("All environment variables are loaded. Starting the server...")

qdrant_client = QdrantClient(
    host=qdrant_host,
    port=qdrant_port,
    api_key=qdrant_api_key,
)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(recoms, prefix='/api/v1/recoms', tags=['recoms'])