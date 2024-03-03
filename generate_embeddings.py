import pika
import json
import pandas as pd
import pickle
import sqlite3
import os
# Get the API key from the global environment variable
import openai
import numpy as np
from openai import OpenAI
from app.main import api_key
# constants
client = OpenAI(api_key=api_key)
EMBEDDING_MODEL = "text-embedding-3-small"

embedding_cache = {}


def poll_and_process():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='articles')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        embedding = openai.Embedding.create(input=data['content'])
        data['embedding'] = embedding['data']
        publish_processed_data(data)

    channel.basic_consume(queue='articles', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def publish_processed_data(data):
    # Similar to publish_to_queue, but targets a different queue/storage
    pass

poll_and_process()
