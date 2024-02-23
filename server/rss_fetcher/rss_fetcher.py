import feedparser
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime, timedelta
import pytz
import uuid
import weaviate
import json
 
import time
 
def wait_for_weaviate():
    """Wait until Weaviate is available."""
   
    while True:
        try:
            # Try fetching the Weaviate metadata without initiating the client here
            response = requests.get("http://weaviate:8080/v1/meta")
            response.raise_for_status()
            meta = response.json()
           
            # If successful, the instance is up and running
            if meta:
                print("Weaviate is up and running!")
                return
 
        except (requests.exceptions.RequestException):
            # If there's any error (connection, timeout, etc.), wait and try again
            print("Waiting for Weaviate...")
            time.sleep(5)
 
RSS_URLS = [
    "https://thedefiant.io/api/feed",
    "https://cointelegraph.com/rss",
    "https://cryptopotato.com/feed/",
    "https://cryptoslate.com/feed/",
    "https://cryptonews.com/news/feed/",
    "https://smartliquidity.info/feed/",
    "https://bitcoinmagazine.com/feed",
    "https://decrypt.co/feed",
    "https://bitcoinist.com/feed/",
    "https://www.newsbtc.com/feed/",
    "https://cryptobriefing.com/feed",
    "https://coinjournal.net/feed/",
    "https://ambcrypto.com/feed/",
    "https://www.the-blockchain.com/feed/"
]
 
def get_article_body(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'}
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
 
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
 
        # Directly return list of non-empty paragraphs
        return [p.get_text().strip() for p in paragraphs if p.get_text().strip() != ""]
 
    except Exception as e:
        print(f"Error fetching article body for {link}. Reason: {e}")
        return []
 
def parse_date(date_str):
    # Current date format from the RSS
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    try:
        dt = datetime.strptime(date_str, date_format)
        # Ensure the datetime is in UTC
        return dt.astimezone(pytz.utc)
    except ValueError:
        # Attempt to handle other possible formats
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        dt = datetime.strptime(date_str, date_format)
        return dt.replace(tzinfo=pytz.utc)
 
def fetch_rss(from_datetime=None):
    all_data = []
    all_entries = []
   
    # Step 1: Fetch all the entries from the RSS feeds and filter them by date.
    for url in RSS_URLS:
        print(f"Fetching {url}")
        feed = feedparser.parse(url)
        entries = feed.entries
        print('feed.entries', len(entries))
 
        for entry in feed.entries:
            entry_date = parse_date(entry.published)
           
            # Filter the entries based on the provided date
            if from_datetime and entry_date <= from_datetime:
                continue
 
            # Storing only necessary data to minimize memory usage
            all_entries.append({
                "Title": entry.title,
                "Link": entry.link,
                "Summary": entry.summary,
                "PublishedDate": entry.published
            })
 
    # Step 2: Shuffle the filtered entries.
    random.shuffle(all_entries)
 
    # Step 3: Extract the body for each entry and break it down by paragraphs.
    for entry in all_entries:
        article_body = get_article_body(entry["Link"])
 
        print("\\nTitle:", entry["Title"])
        print("Link:", entry["Link"])
        print("Summary:", entry["Summary"])
        print("Published Date:", entry["PublishedDate"])
 
        # Create separate records for each paragraph
        for paragraph in article_body:
            data = {
                "UUID": str(uuid.uuid4()), # UUID for each paragraph
                "Title": entry["Title"],
                "Link": entry["Link"],
                "Summary": entry["Summary"],
                "PublishedDate": entry["PublishedDate"],
                "Body": paragraph
            }
            all_data.append(data)
 
    print("-" * 50)
 
    df = pd.DataFrame(all_data)
    return df
 
def insert_data(df,batch_size=100):
    # Initialize the batch process
    with client.batch as batch:
        batch.batch_size = 100
 
        # Loop through and batch import the 'RSS_Entry' data
        for i, row in df.iterrows():
            if i%100==0:
                print(f"Importing entry: {i+1}")  # Status update
 
            properties = {
                "UUID": row["UUID"],
                "Title": row["Title"],
                "Link": row["Link"],
                "Summary": row["Summary"],
                "PublishedDate": row["PublishedDate"],
                "Body": row["Body"]
            }
 
            client.batch.add_data_object(properties, "RSS_Entry")
 
if __name__ == "__main__":
 
    # Wait until weaviate is available
    wait_for_weaviate()
 
    # Initialize the Weaviate client
    client = weaviate.Client("http://weaviate:8080")
    client.timeout_config = (3, 200)
 
    # Reset the schema
    client.schema.delete_all()
 
    # Define the "RSS_Entry" class
    class_obj = {
        "class": "RSS_Entry",
        "description": "An entry from an RSS feed",
        "properties": [
            {"dataType": ["text"], "description": "UUID of the entry", "name": "UUID"},
            {"dataType": ["text"], "description": "Title of the entry", "name": "Title"},
            {"dataType": ["text"], "description": "Link of the entry", "name": "Link"},
            {"dataType": ["text"], "description": "Summary of the entry", "name": "Summary"},
            {"dataType": ["text"], "description": "Published Date of the entry", "name": "PublishedDate"},
            {"dataType": ["text"], "description": "Body of the entry", "name": "Body"}
        ],
        "vectorizer": "text2vec-transformers"
    }
 
    # Add the schema
    client.schema.create_class(class_obj)
 
    # Retrieve the schema
    schema = client.schema.get()
    # Display the schema
    print(json.dumps(schema, indent=4))
    print("-"*50)
 
    # Current datetime
    now = datetime.now(pytz.utc)
 
    # Fetching articles from the last days
    days_ago = 3
    print(f"Getting historical data for the last {days_ago} days ago.")
    last_week = now - timedelta(days=days_ago)
    df_hist =  fetch_rss(last_week)
 
    print("Head")
    print(df_hist.head().to_string())
    print("Tail")
    print(df_hist.head().to_string())
    print("-"*50)
    print("Total records fetched:",len(df_hist))
    print("-"*50)
    print("Inserting data")
 
    # insert historical data
    insert_data(df_hist,batch_size=100)
 
    print("-"*50)
    print("Data Inserted")
 
    # check if there is any relevant news in the last minute
 
    while True:
        # Current datetime
        now = datetime.now(pytz.utc)
 
        # Fetching articles from the last hour
        one_min_ago = now - timedelta(minutes=1)
        df =  fetch_rss(one_min_ago)
        print("Head")
        print(df.head().to_string())
        print("Tail")
        print(df.head().to_string())
       
        print("Inserting data")
 
        # insert minute data
        insert_data(df,batch_size=100)
 
        print("data inserted")
 
        print("-"*50)
 
        # Sleep for a minute
        time.sleep(60)