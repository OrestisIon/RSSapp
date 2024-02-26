import feedparser
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime, timedelta
import pytz
import uuid
from qdrant_client import QdrantClient
import json
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import time
import tiktoken

# imports from langchain package

from langchain.prompts import PromptTemplate



def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
 
def wait_for_qdrant():
    """Wait until Qdrant is available."""
   
    while True:
        try:
            # Try fetching the Weaviate metadata without initiating the client here
            response = requests.get("http://127.0.0.1:6333/")
            response.raise_for_status()
            meta = response.json()
           
            # If successful, the instance is up and running
            if meta:
                print("Qdrant is up and running!")
                return
 
        except (requests.exceptions.RequestException):
            # If there's any error (connection, timeout, etc.), wait and try again
            print("Waiting for Qdrant...")
            time.sleep(5)
 
RSS_URLS = ["http://feeds.abcnews.com/abcnews/usheadlines", "http://rss.cnn.com/rss/cnn_topstories.rss", "http://www.cbsnews.com/latest/rss/main", "http://www.nytimes.com/services/xml/rss/nyt/National.xml", "http://online.wsj.com/xml/rss/3_7085.xml", "http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news2", "http://rss.csmonitor.com/feeds/usa", "http://feeds.nbcnews.com/feeds/topstories", "http://feeds.nbcnews.com/feeds/worldnews", "http://feeds.reuters.com/Reuters/worldNews", "http://feeds.reuters.com/Reuters/domesticNews", "http://hosted.ap.org/lineups/USHEADS.rss", "http://hosted.ap.org/lineups/WORLDHEADS.rss", "http://www.huffingtonpost.com/feeds/verticals/world/index.xml", "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml", "http://news.yahoo.com/rss/us", "http://rss.news.yahoo.com/rss/world", "http://www.newsweek.com/rss", "http://feeds.feedburner.com/thedailybeast/articles", "http://qz.com/feed", "http://www.theguardian.com/world/usa/rss", "http://www.politico.com/rss/politicopicks.xml", "http://www.newyorker.com/feed/news", "http://feeds.feedburner.com/NationPBSNewsHour", "http://feeds.feedburner.com/NewshourWorld", "http://www.usnews.com/rss/news", "http://www.npr.org/rss/rss.php?id=1003", "http://www.npr.org/rss/rss.php?id=1004", "http://feeds.feedburner.com/AtlanticNational", "http://feeds.feedburner.com/TheAtlanticWire", "http://www.latimes.com/nation/rss2.0.xml", "http://www.latimes.com/world/rss2.0.xml", "http://api.breakingnews.com/api/v1/item/?format=rss", "https://news.vice.com/rss", "http://talkingpointsmemo.com/feed/livewire", "http://www.salon.com/category/news/feed/rss/", "http://time.com/newsfeed/feed/", "http://feeds.foxnews.com/foxnews/latest?format=xml", "http://mashable.com/us-world/rss/", "http://www.politico.com/rss/magazine.xml", "http://www.politico.com/rss/Top10Blogs.xml", "http://www.huffingtonpost.com/feeds/verticals/politics/index.xml", "http://rss.cnn.com/rss/cnn_allpolitics.rss", "http://www.buzzfeed.com/politics.xml", "http://feeds.nbcnews.com/feeds/nbcpolitics", "http://feeds.foxnews.com/foxnews/politics", "http://feeds.washingtonpost.com/rss/rss_election-2012", "http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "http://rss.nytimes.com/services/xml/rss/nyt/Upshot.xml", "http://thecaucus.blogs.nytimes.com/feed/", "http://feeds.reuters.com/Reuters/PoliticsNews", "http://blogs.wsj.com/washwire/feed/?mod=WSJ_Politics%2520and%2520Policy", "http://www.reddit.com/r/politics/.rss", "http://feeds.dailykos.com/dailykos/index.xml", "http://www.npr.org/rss/rss.php?id=1014", "http://www.npr.org/rss/rss.php?id=5", "http://www.rollcall.com/rss/all_news.xml", "http://www.rollcall.com/news/?zkDo=showRSS", "http://www.rollcall.com/politics/archives/?zkDo=showRSS", "http://www.rollcall.com/policy/archives/?zkDo=showRSS", "http://www.nationaljournal.com/?rss=1", "http://www.nationaljournal.com/white-house?rss=1", "http://www.nationaljournal.com/congress?rss=1", "http://www.nationaljournal.com/politics?rss=1", "http://www.nationaljournal.com/congressional-connection?rss=1", "http://www.thenation.com/rss/articles", "http://www.thenation.com/blogs/rss/politics", "http://www.thenation.com/blogs/rss/foreign-reporting", "http://www.washingtontimes.com/rss/headlines/news/politics/", "http://feeds.feedburner.com/realclearpolitics/qlMj", "http://feeds.feedburner.com/BreitbartFeed", "http://dailycaller.com/section/politics/feed/", "https://www.nationalreview.com/rss.xml", "http://feeds.feedburner.com/DrudgeReportFeed", "http://www.weeklystandard.com/rss/site.xml", "http://www.usnews.com/blogrss/washington-whispers", "http://http://www.usnews.com/blogrss/ballot-2014", "http://feeds.slate.com/slate-101526", "http://feeds.feedburner.com/motherjones/Politics", "http://www.newrepublic.com/taxonomy/term/17538/feed", "http://fivethirtyeight.com/politics/feed/", "http://www.redstate.com/feed/", "http://humanevents.com/feed/", "http://twitchy.com/category/us-politics/feed/", "http://talkingpointsmemo.com/feed/all", "http://hosted2.ap.org/atom/APDEFAULT/f70471f764144b2fab526d39972d37b3", "http://online.wsj.com/xml/rss/3_7014.xml", "http://www.nytimes.com/services/xml/rss/nyt/Business.xml", "http://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "http://feeds.reuters.com/reuters/businessNews", "http://feeds.washingtonpost.com/rss/rss_storyline", "http://feeds.washingtonpost.com/rss/rss_wonkblog", "http://www.economist.com/feeds/print-sections/77/business.xml", "http://www.business-standard.com/rss/latest.rss", "http://www.business-standard.com/rss/home_page_top_stories.rss", "http://feeds.harvardbusiness.org/harvardbusiness?format=xml", "http://au.ibtimes.com/rss/articles/region/1.rss", "http://www.businessweek.com/search/rssfeed.htm", "http://www.huffingtonpost.com/feeds/verticals/business/news.xml", "http://www.ft.com/rss/home/us", "http://rss.cnn.com/rss/edition_business.rss", "http://www.bloomberg.com/feed/podcast/law.xml", "http://www.health.harvard.edu/rss.php", "http://www.health.com/health/healthy-happy/feed", "http://rss.cnn.com/rss/cnn_health.rss", "http://www.nytimes.com/services/xml/rss/nyt/Health.xml", "http://www.forbes.com/health/feed2/", "http://feeds.bbci.co.uk/news/health/rss.xml?edition=us", "http://feeds.abcnews.com/abcnews/healthheadlines", "http://feeds.nbcnews.com/feeds/health", "http://feeds.reuters.com/reuters/healthNews", "http://www.chicagotribune.com/lifestyles/health/rss2.0.xml", "http://feeds.huffingtonpost.com/c/35496/f/677071/index.rss", "http://www.theguardian.com/society/health/rss", "http://www.nydailynews.com/lifestyle/health/index_rss.xml", "http://www.menshealth.com/events-promotions/washpofeed", "http://feeds.glamour.com/glamour/health_fitness", "http://feeds.newscientist.com/health", "http://time.com/health/feed/", "http://hosted2.ap.org/atom/APDEFAULT/bbd825583c8542898e6fa7d440b9febc", "http://www.womenshealthandfitness.com.au/component/obrss/women-s-health-fitness-combined-feed", "http://www.usnews.com/rss/health?int=a7fe09", "http://news.yahoo.com/rss/health", "http://www.wsj.com/xml/rss/3_7201.xml", "http://www.healthcareitnews.com/home/feed", "http://www.modernhealthcare.com/section/rss01&mime=xml", "http://www.mayoclinic.org/rss/all-health-information-topics", "http://feeds.sciencedaily.com/sciencedaily/top_news/top_health", "http://khn.org/feed/", "http://feeds.lexblog.com/foodsafetynews/mRcs", "http://feeds.washingtonpost.com/rss/lifestyle", "http://www.buzzfeed.com/health.xml", "http://vitals.lifehacker.com/rss", "http://www.self.com/feed/fitness-news/", "http://feeds.huffingtonpost.com/c/35496/f/677070/index.rss", "http://www.cpsc.gov/en/Newsroom/CPSC-RSS-Feed/Recalls-RSS/", "http://www.medpagetoday.com/rss/Headlines.xml", "http://www.medscape.com/cx/rssfeeds/2700.xml", "http://rss.nytimes.com/services/xml/rss/nyt/Health.xml", "http://www.theguardian.com/lifeandstyle/health-and-wellbeing/rss", "http://rss.medicalnewstoday.com/featurednews.xml", "http://www.npr.org/rss/rss.php?id=1128"]

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
 
def getEntries():
    feedlist = RSS_URLS[:5]
    for feed in feedlist:
        feed = feedparser.parse(feed)
        print(feed.keys())

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
 
def fetch_rss(urls,from_datetime=None):
    all_data = []
    all_entries = []
   
    # Step 1: Fetch all the entries from the RSS feeds and filter them by date.
    for url in urls:
        print(f"Fetching {url}")
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"Error fetching {url}. Reason: {e}")
            continue
        entries = feed.entries
        print('feed.entries', len(entries))
        if len(entries) == 0:
            print(f"No entries found in {url}")
            continue
 
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
            print("Paragraph:", paragraph[:100] + "..." if len(paragraph) > 100 else paragraph)
            print("Number of tokens:", num_tokens_from_string(paragraph, "cl100k_base"))
        print("Title:", entry["Title"])
        print("Number of paragraphs:", len(article_body))
        
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
    first10 = RSS_URLS[:10]
    fetch_rss(first10)
 
# if __name__ == "__main__":
 
#     # Wait until weaviate is available
#     wait_for_qdrant()
 
#     # Initialize the Weaviate client
#     client = QdrantClient("localhost", port=6333) 
#     # Reset the schema
#     client.schema.delete_all()
#     client.create_collection(
#         collection_name="rss_collection",
#         vectors_config=VectorParams(size=4, distance=Distance.DOT),
#     )

 
#     # Define the "RSS_Entry" class
#     class_obj = {
#         "class": "RSS_Entry",
#         "description": "An entry from an RSS feed",
#         "properties": [
#             {"dataType": ["text"], "description": "UUID of the entry", "name": "UUID"},
#             {"dataType": ["text"], "description": "Title of the entry", "name": "Title"},
#             {"dataType": ["text"], "description": "Link of the entry", "name": "Link"},
#             {"dataType": ["text"], "description": "Summary of the entry", "name": "Summary"},
#             {"dataType": ["text"], "description": "Published Date of the entry", "name": "PublishedDate"},
#             {"dataType": ["text"], "description": "Body of the entry", "name": "Body"}
#         ],
#         "vectorizer": "text2vec-transformers"
#     }
 
#     # Add the schema
#     client.schema.create_class(class_obj)
 
#     # Retrieve the schema
#     schema = client.schema.get()
#     # Display the schema
#     print(json.dumps(schema, indent=4))
#     print("-"*50)
 
#     # Current datetime
#     now = datetime.now(pytz.utc)
 
#     # Fetching articles from the last days
#     days_ago = 3
#     print(f"Getting historical data for the last {days_ago} days ago.")
#     last_week = now - timedelta(days=days_ago)
#     df_hist =  fetch_rss(last_week)
 
#     print("Head")
#     print(df_hist.head().to_string())
#     print("Tail")
#     print(df_hist.head().to_string())
#     print("-"*50)
#     print("Total records fetched:",len(df_hist))
#     print("-"*50)
#     print("Inserting data")
 
#     # insert historical data
#     insert_data(df_hist,batch_size=100)
 
#     print("-"*50)
#     print("Data Inserted")
 
#     # check if there is any relevant news in the last minute
 
#     while True:
#         # Current datetime
#         now = datetime.now(pytz.utc)
 
#         # Fetching articles from the last hour
#         one_min_ago = now - timedelta(minutes=1)
#         df =  fetch_rss(one_min_ago)
#         print("Head")
#         print(df.head().to_string())
#         print("Tail")
#         print(df.head().to_string())
       
#         print("Inserting data")
 
#         # insert minute data
#         insert_data(df,batch_size=100)
 
#         print("data inserted")
 
#         print("-"*50)
 
#         # Sleep for a minute
#         time.sleep(60)