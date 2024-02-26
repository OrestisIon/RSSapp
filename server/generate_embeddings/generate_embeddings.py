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

api_key = userdata.get('OPENAI_API_KEY')  # Make sure this line correctly fetches your API key
if api_key is not None:
    print ("OPENAI_API_KEY is ready")
else:
    print ("OPENAI_API_KEY environment variable not found")

client = OpenAI(api_key=api_key)

# constants
EMBEDDING_MODEL = "text-embedding-3-small"

embedding_cache = {}
openai.api_key = 'your_openai_api_key'

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
