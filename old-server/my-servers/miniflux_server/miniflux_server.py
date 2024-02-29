import miniflux
# load API key using dotenv
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("MINIFLUX_API_KEY")
URL = os.getenv("MINIFLUX_URL")
def get_client(usr, pswd):
    #  Error checking for the user and password
    if usr is None or pswd is None:
        raise ValueError("Username and password cannot be None")
    try:
        client = miniflux.Client(URL, usr, pswd)
        return client
    except Exception as e:
        print(f"Error fetching authenticating user. Reason: {e}")
def get_feeds(client):
    try:
        feeds = client.get_feeds()
        return feeds
    except Exception as e:
        print(f"Error fetching feeds. Reason: {e}")
        
def (client, feed_id, category_id):
# Authentication using username/password
client = miniflux.Client(URL, "my_username", "my_secret_password")

# Authentication using an API token
client = miniflux.Client(URL, api_key="My Secret Token")

# Get all feeds
feeds = client.get_feeds()

# Refresh a feed
client.refresh_feed(123)

# Discover subscriptions from a website
subscriptions = client.discover("https://example.org")

# Create a new feed, with a personalized user agent and with the crawler enabled
feed_id = client.create_feed("http://example.org/feed.xml", 42, crawler=True, user_agent="GoogleBot")

# Fetch 10 starred entries
entries = client.get_entries(starred=True, limit=10)

# Fetch last 5 feed entries
feed_entries = client.get_feed_entries(123, direction='desc', order='published_at', limit=5)

# Update a feed category
client.update_feed(123, category_id=456)

# main
# parameters username and password
if __name__ == "__main__":
    client = get_client("my_username", "my_secret_password")
    feeds = get_feeds(client)
    print(feeds)