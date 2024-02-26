import feedparser
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import pika  # For RabbitMQ
import json
from bs4 import BeautifulSoup
import pytz
import uuid
import random
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
from threading import Lock
import logging
import sys
import requests


# Basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s')

banned_feeds_lock = Lock()


ALL_BANNED_FEEDS = []
rss_urls = []
def get_article_body(link):
    try:
        logging.info(f"Thread {link}: starting")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'}
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
 
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        # if the article body has less than 3 paragraphs, it's likely not an article
        if len(paragraphs) < 3:
            return []
        logging.info(f"Thread {link}: finishing")
        # Directly return list of non-empty paragraphs
        return [p.get_text().strip() for p in paragraphs if p.get_text().strip() != ""]
 
    except Exception as e:
        print(f"Error fetching article body for {link}. Reason: {e}")
        logging.info(f"Thread {link}: finishing")

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
 

def fetch_rss_parallel(urls, from_datetime=None):
    all_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(fetch_rss_single, url, from_datetime): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            all_data.extend(future.result())
    return all_data


def get_article_body_parallel(entries):
    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        results = list(executor.map(get_article_body, [entry["Link"] for entry in entries]))
    return results  # Exclude empty results



def fetch_rss_single(url,from_datetime=None):
    all_entries = []
    # Step 1: Fetch all the entries from the RSS feeds and filter them by date.
    print(f"Fetching {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'}
        feedparser.api._open_resource = lambda *args, **kwargs: requests.get(args[0], headers=headers, timeout=5).content
        feed = feedparser.parse(url)
        entries = feed.entries
        print('feed.entries', len(entries))
        # cap the number of entries to 10
        if len(entries) > 100:
            entries = entries[:100]
        for entry in feed.entries:
            # Filter the entries based on the provided date
            if from_datetime and entry_date <= from_datetime:
                continue
            # Check if all necessary attributes exist in the entry
            if not all(hasattr(entry, attr) for attr in ["title", "link", "summary", "published"]):
                continue
            entry_date = parse_date(entry.published)
            # Storing only necessary data to minimize memory usage
            all_entries.append({
                "Title": entry.title,
                "Link": entry.link,
                "Summary": entry.summary,
                "PublishedDate": entry.published
            })
    except Exception as e:
        print(f"Error fetching {url}. Reason: {e}")
    if len(all_entries) == 0:
        with banned_feeds_lock:
            ALL_BANNED_FEEDS.append(url)
    return all_entries

def publish_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='articles')
    channel.basic_publish(exchange='',
                          routing_key='articles',
                          body=json.dumps(data))
    connection.close()


def scrape_and_publish(num=10):
    df = pd.read_csv('./data/cache_feeds.csv')
    len_df = len(df)
    if len(df) == 0:
        print("No feeds more feeds to scrape")
        return
    for i in range(0, len_df, num):
        # Load the data from the RSS feeds csv file
        df = pd.read_csv('./data/cache_feeds.csv')
        df_old = pd.read_csv('./data/feeds_done.csv')
        # remove all the entries of the df whose url is in df_old
        df = df[~df['urls'].isin(df_old['urls'])]
        df = df[:num]
        # Separate the DataFrame based on the value of the to_scrap column
        to_scrap_df = df[df['to_scrape'] == True]
        not_to_scrap_df = df[df['to_scrape'] == False]
        entriesa =  fetch_rss_parallel(to_scrap_df['urls'].tolist())
        entriesb =  fetch_rss_parallel(not_to_scrap_df['urls'].tolist())
        # get the bodies only for the articles that are to be scrapped
        bodies = get_article_body_parallel(entriesa)
        # Save the articles to a csv file
        articles = []
        removed = []
        for i, entry in enumerate(entriesa):
            if entry["Link"] in removed:
                bodies[i] = []
            # if the article body is empty, set the to_scrap column to False
            elif len(bodies[i]) == 0:
                removed.append(entry["Link"])
            articles.append({
                "Title": entry["Title"],
                "Link": entry["Link"],
                "Summary": entry["Summary"],
                "PublishedDate": entry["PublishedDate"],
                "Body": bodies[i]
            })
        for i, entry in enumerate(entriesb):
            articles.append({
                "Title": entry["Title"],
                "Link": entry["Link"],
                "Summary": entry["Summary"],
                "PublishedDate": entry["PublishedDate"],
                "Body": []
            })
        # adjust the to_scrap column based on the removed articles
        for url in removed:
            df.loc[df['urls'] == url, 'to_scrape'] = False
        # Remove the df from the cache_feeds.csv file
        dfn = pd.read_csv('./data/cache_feeds.csv')
        dfn = dfn[~dfn['urls'].isin(df['urls'])]
        dfn.to_csv('./data/cache_feeds.csv', index=False )
        
        with banned_feeds_lock:
            # remove all the entries of the df whose url is in the banned list
            df = df[~df['urls'].isin(ALL_BANNED_FEEDS)]
        # append the df to the feeds_done.csv file
        df.to_csv('./data/feeds_done.csv',mode='a', index=False, header=False)
        df = pd.DataFrame(articles)
        df.to_csv('./data/articles.csv',mode='a', index=False, header=False)
        # publish_to_queue(df.to_dict(orient='records'))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    else:
        num = 10
    scrape_and_publish(num)
    # Schedule the scraping and publishing job
    # scheduler = BlockingScheduler()
    # scheduler.add_job(scrape_and_publish, 'interval', days=1)  # Run every hour
    # scheduler.start()