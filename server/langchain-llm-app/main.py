# from langchain.llms import OpenAI
# from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import openai
from typing import List, Iterator
import pandas as pd
import numpy as np
import os
import wget
from ast import literal_eval


client = QdrantClient("localhost", port=6333)
RSS_URLS = ["http://feeds.abcnews.com/abcnews/usheadlines", "http://rss.cnn.com/rss/cnn_topstories.rss", "http://www.cbsnews.com/latest/rss/main", "http://www.nytimes.com/services/xml/rss/nyt/National.xml", "http://online.wsj.com/xml/rss/3_7085.xml", "http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news2", "http://rss.csmonitor.com/feeds/usa", "http://feeds.nbcnews.com/feeds/topstories", "http://feeds.nbcnews.com/feeds/worldnews", "http://feeds.reuters.com/Reuters/worldNews", "http://feeds.reuters.com/Reuters/domesticNews", "http://hosted.ap.org/lineups/USHEADS.rss", "http://hosted.ap.org/lineups/WORLDHEADS.rss", "http://www.huffingtonpost.com/feeds/verticals/world/index.xml", "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml", "http://news.yahoo.com/rss/us", "http://rss.news.yahoo.com/rss/world", "http://www.newsweek.com/rss", "http://feeds.feedburner.com/thedailybeast/articles", "http://qz.com/feed", "http://www.theguardian.com/world/usa/rss", "http://www.politico.com/rss/politicopicks.xml", "http://www.newyorker.com/feed/news", "http://feeds.feedburner.com/NationPBSNewsHour", "http://feeds.feedburner.com/NewshourWorld", "http://www.usnews.com/rss/news", "http://www.npr.org/rss/rss.php?id=1003", "http://www.npr.org/rss/rss.php?id=1004", "http://feeds.feedburner.com/AtlanticNational", "http://feeds.feedburner.com/TheAtlanticWire", "http://www.latimes.com/nation/rss2.0.xml", "http://www.latimes.com/world/rss2.0.xml", "http://api.breakingnews.com/api/v1/item/?format=rss", "https://news.vice.com/rss", "http://talkingpointsmemo.com/feed/livewire", "http://www.salon.com/category/news/feed/rss/", "http://time.com/newsfeed/feed/", "http://feeds.foxnews.com/foxnews/latest?format=xml", "http://mashable.com/us-world/rss/", "http://www.politico.com/rss/magazine.xml", "http://www.politico.com/rss/Top10Blogs.xml", "http://www.huffingtonpost.com/feeds/verticals/politics/index.xml", "http://rss.cnn.com/rss/cnn_allpolitics.rss", "http://www.buzzfeed.com/politics.xml", "http://feeds.nbcnews.com/feeds/nbcpolitics", "http://feeds.foxnews.com/foxnews/politics", "http://feeds.washingtonpost.com/rss/rss_election-2012", "http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "http://rss.nytimes.com/services/xml/rss/nyt/Upshot.xml", "http://thecaucus.blogs.nytimes.com/feed/", "http://feeds.reuters.com/Reuters/PoliticsNews", "http://blogs.wsj.com/washwire/feed/?mod=WSJ_Politics%2520and%2520Policy", "http://www.reddit.com/r/politics/.rss", "http://feeds.dailykos.com/dailykos/index.xml", "http://www.npr.org/rss/rss.php?id=1014", "http://www.npr.org/rss/rss.php?id=5", "http://www.rollcall.com/rss/all_news.xml", "http://www.rollcall.com/news/?zkDo=showRSS", "http://www.rollcall.com/politics/archives/?zkDo=showRSS", "http://www.rollcall.com/policy/archives/?zkDo=showRSS", "http://www.nationaljournal.com/?rss=1", "http://www.nationaljournal.com/white-house?rss=1", "http://www.nationaljournal.com/congress?rss=1", "http://www.nationaljournal.com/politics?rss=1", "http://www.nationaljournal.com/congressional-connection?rss=1", "http://www.thenation.com/rss/articles", "http://www.thenation.com/blogs/rss/politics", "http://www.thenation.com/blogs/rss/foreign-reporting", "http://www.washingtontimes.com/rss/headlines/news/politics/", "http://feeds.feedburner.com/realclearpolitics/qlMj", "http://feeds.feedburner.com/BreitbartFeed", "http://dailycaller.com/section/politics/feed/", "https://www.nationalreview.com/rss.xml", "http://feeds.feedburner.com/DrudgeReportFeed", "http://www.weeklystandard.com/rss/site.xml", "http://www.usnews.com/blogrss/washington-whispers", "http://http://www.usnews.com/blogrss/ballot-2014", "http://feeds.slate.com/slate-101526", "http://feeds.feedburner.com/motherjones/Politics", "http://www.newrepublic.com/taxonomy/term/17538/feed", "http://fivethirtyeight.com/politics/feed/", "http://www.redstate.com/feed/", "http://humanevents.com/feed/", "http://twitchy.com/category/us-politics/feed/", "http://talkingpointsmemo.com/feed/all", "http://hosted2.ap.org/atom/APDEFAULT/f70471f764144b2fab526d39972d37b3", "http://online.wsj.com/xml/rss/3_7014.xml", "http://www.nytimes.com/services/xml/rss/nyt/Business.xml", "http://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "http://feeds.reuters.com/reuters/businessNews", "http://feeds.washingtonpost.com/rss/rss_storyline", "http://feeds.washingtonpost.com/rss/rss_wonkblog", "http://www.economist.com/feeds/print-sections/77/business.xml", "http://www.business-standard.com/rss/latest.rss", "http://www.business-standard.com/rss/home_page_top_stories.rss", "http://feeds.harvardbusiness.org/harvardbusiness?format=xml", "http://au.ibtimes.com/rss/articles/region/1.rss", "http://www.businessweek.com/search/rssfeed.htm", "http://www.huffingtonpost.com/feeds/verticals/business/news.xml", "http://www.ft.com/rss/home/us", "http://rss.cnn.com/rss/edition_business.rss", "http://www.bloomberg.com/feed/podcast/law.xml", "http://www.health.harvard.edu/rss.php", "http://www.health.com/health/healthy-happy/feed", "http://rss.cnn.com/rss/cnn_health.rss", "http://www.nytimes.com/services/xml/rss/nyt/Health.xml", "http://www.forbes.com/health/feed2/", "http://feeds.bbci.co.uk/news/health/rss.xml?edition=us", "http://feeds.abcnews.com/abcnews/healthheadlines", "http://feeds.nbcnews.com/feeds/health", "http://feeds.reuters.com/reuters/healthNews", "http://www.chicagotribune.com/lifestyles/health/rss2.0.xml", "http://feeds.huffingtonpost.com/c/35496/f/677071/index.rss", "http://www.theguardian.com/society/health/rss", "http://www.nydailynews.com/lifestyle/health/index_rss.xml", "http://www.menshealth.com/events-promotions/washpofeed", "http://feeds.glamour.com/glamour/health_fitness", "http://feeds.newscientist.com/health", "http://time.com/health/feed/", "http://hosted2.ap.org/atom/APDEFAULT/bbd825583c8542898e6fa7d440b9febc", "http://www.womenshealthandfitness.com.au/component/obrss/women-s-health-fitness-combined-feed", "http://www.usnews.com/rss/health?int=a7fe09", "http://news.yahoo.com/rss/health", "http://www.wsj.com/xml/rss/3_7201.xml", "http://www.healthcareitnews.com/home/feed", "http://www.modernhealthcare.com/section/rss01&mime=xml", "http://www.mayoclinic.org/rss/all-health-information-topics", "http://feeds.sciencedaily.com/sciencedaily/top_news/top_health", "http://khn.org/feed/", "http://feeds.lexblog.com/foodsafetynews/mRcs", "http://feeds.washingtonpost.com/rss/lifestyle", "http://www.buzzfeed.com/health.xml", "http://vitals.lifehacker.com/rss", "http://www.self.com/feed/fitness-news/", "http://feeds.huffingtonpost.com/c/35496/f/677070/index.rss", "http://www.cpsc.gov/en/Newsroom/CPSC-RSS-Feed/Recalls-RSS/", "http://www.medpagetoday.com/rss/Headlines.xml", "http://www.medscape.com/cx/rssfeeds/2700.xml", "http://rss.nytimes.com/services/xml/rss/nyt/Health.xml", "http://www.theguardian.com/lifeandstyle/health-and-wellbeing/rss", "http://rss.medicalnewstoday.com/featurednews.xml", "http://www.npr.org/rss/rss.php?id=1128"]
def addFilter():
    search_result = client.search(
        collection_name="test_collection",
        query_vector=[0.2, 0.1, 0.9, 0.7],
        query_filter=Filter(
            must=[FieldCondition(key="city", match=MatchValue(value="London"))]
        ),
        with_payload=True,
        limit=3,
    )

    print(search_result)
    
def runQuery():
    search_result = client.search(
        collection_name="test_collection1", query_vector=[0.2, 0.1, 0.9, 0.7], limit=3
    )
    print(search_result)

def deleteCollection():
    client.delete_collection(collection_name="test_collection1")
    
if __name__ == "__main__":
    deleteCollection()
    client.create_collection(
        collection_name="test_collection1",
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )

    operation_info = client.upsert(
        collection_name="test_collection1",
        wait=True,
        points=[
            PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
            PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
            PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
            PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
            PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
            PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
        ],
    )
    print(operation_info)
    runQuery()
    addFilter()
    

    





    
    