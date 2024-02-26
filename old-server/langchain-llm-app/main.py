# from langchain.llms import OpenAI
# from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import openai as OpenAI
from typing import List, Iterator
import pandas as pd
import numpy as np
import os
import wget
from ast import literal_eval
from dotenv import load_dotenv
from qdrant_client.http.models import Batch


api_key = os.getenv("OPENAI_API_KEY")
qdrant_client = QdrantClient("localhost", port=6333)
openai_client = OpenAI(api_key=api_key)

# constants
EMBEDDING_MODEL = "text-embedding-3-large"

embedding_cache = {}
def addFilter():
    search_result = qdrant_client.search(
        collection_name="test_collection",
        query_vector=[0.2, 0.1, 0.9, 0.7],
        query_filter=Filter(
            must=[FieldCondition(key="city", match=MatchValue(value="London"))]
        ),
        with_payload=True,
        limit=3,
    )

    print(search_result)
    
def get_embedding(text, model=EMBEDDING_MODEL): # model = "deployment_name"
    embedding = qdrant_client.embeddings.create(input=[text], model=model).data[0].embedding
    # Convert the embedding to a NumPy array if it's not already
    # if not isinstance(embedding, np.ndarray):
    #     embedding = np.array(embedding)
    return embedding

def runQuery():
    search_result = qdrant_client.search(
        collection_name="test_collection1", query_vector=[0.2, 0.1, 0.9, 0.7], limit=3
    )
    print(search_result)

def deleteCollection():
    qdrant_client.delete_collection(collection_name="test_collection1")
    
if __name__ == "__main__":
    deleteCollection()
    qdrant_client.create_collection(
        collection_name="test_collection1",
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )
    
    response = openai_client.embeddings.create(
        input="The best vector database",
        model=EMBEDDING_MODEL,
    )
    operation_info = qdrant_client.upsert(
        collection_name="MyCollection",
        points=Batch(
            ids=[1],
            vectors=[response.data[0].embedding],
        ),
    )

    print(operation_info)

    

    





    
    