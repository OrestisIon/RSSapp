from app.api.dependencies.auth import validate_is_authenticated
from app.api.dependencies.core import DBSessionDep
from app.crud.user import get_user, create_user
from app.crud.miniflux_manager import get_feed, create_feed, get_all_feeds
from app.schemas.user import User,UserCreate
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.user import CurrentClient, DefaultClient
from app.models.miniflux import Feed, DiscoveredFeed, Category, Icon, Entry, FeedRe
from app.models.user import Feed as FeedSchema
from app.models.user import UserFeed as UserFeedSchema
import miniflux
from typing import List
from app.ml.reccomender import fetch_feed
from app.ml.reccomender import get_recommendations

# TODO 1: Router Create user add MiniFluxClient
# TODO 2: Router Get Feeds from MiniFluxClient
# TODO 3: Router Create Feed from MiniFluxClient
# TODO 4: Router Get Feed Entries from MiniFluxClient

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# @router.get(
#     "/{user_id}",
#     response_model=User,
#     dependencies=[Depends(validate_is_authenticated)],
# )
# async def user_details(
#     user_id: int,
#     db_session: DBSessionDep,
# ):
#     """
#     Get any user details
#     """
#     user = await get_user(db_session, user_id)
#     return user


@router.post("/", response_model=User)
async def register_user(user: UserCreate, db_session: DBSessionDep, client: DefaultClient ):
    """
    Register a new user
    """
    return await create_user(db_session, user, client)


@router.get(
    "/feed/{feed_id}",
    response_model=Feed,
    dependencies=[Depends(validate_is_authenticated)],
)
async def feed(client: DefaultClient, feed_id: int ):
    """
    Register a new user
    """
    return await get_feed(client, feed_id)

@router.get(
    "/feeds",
    response_model=List[Feed],
    dependencies=[Depends(validate_is_authenticated)],
)
async def feed(client: DefaultClient, feed_id: int ):
    """
    Register a new user
    """
    return await get_all_feeds(client, feed_id)




@router.get(
    "/discover",
    response_model=Feed,
    dependencies=[Depends(validate_is_authenticated)],
)
async def discover_feed(client: DefaultClient, website_url: str,**kwargs) -> List[DiscoveredFeed]:
    try:
        discovered_feed = await client.discover(website_url, **kwargs)
        return discovered_feed
    except Exception as e:
        print(f"Error discovering feed. Reason: {e}")
        return []

@router.put(
    "/entries",
    response_model=Feed,
    dependencies=[Depends(validate_is_authenticated)],
)




@router.post("/get_feed_recommendations", 
             dependencies=[Depends(validate_is_authenticated)], 
             )
async def genR( db_session: DBSessionDep, user: User = Depends(validate_is_authenticated) ):
    # get user feeds
    feed_ids = db_session.query(UserFeedSchema).filter(UserFeedSchema.user_id == user.id).limit(10).all()
    # Get the feeds from Feed table
    feeds = db_session.query(FeedSchema).filter(FeedSchema.id.in_(feed_ids), FeedSchema.is_scrape == True).limit(5).all()
    response = []
    for feed in feeds:
        # get recommendations for each feed
        entries = await get_recommendations(feed.embedding)
        response.append({"generalTitle":feed.title, "blogs": entries})
    
    # call pinecone for recommendations
    return response




# @router.post("/get_starred_recommendations", response_model=User)
# async def register_user(user: UserCreate, db_session: DBSessionDep, client: DefaultClient ):
#     # get user starred feeds
    
#     # make embeddings
    
#     # call pinecone for recommendations
    
#     return await create_user(db_session, user, client)


@router.post(
    "/feeds", 
    dependencies=[Depends(validate_is_authenticated)])
async def add_feed(feed_url: str, db: DBSessionDep, client: DefaultClient, user: User = Depends(validate_is_authenticated)):
    try:
        response = client.create_feed(feed_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating feed. Reason: {e}")
    
    # Check if the feed already exists based on unique fields, e.g., feed_url
    db_feed = db.query(FeedSchema).filter(FeedSchema.feed_url == feed_url).first()  
    if not db_feed:
        # If the feed does not exist, scrape new feed data
        scraped_feed = await fetch_feed(feed_url)
        # Create a new Feed instance with scraped data
        # Assume scraped_data contains keys that match the Feed model's columns
        db_feed = Feed(scraped_feed)
        # Add the new Feed to the session
        db.add(db_feed)
        db.commit()
        db.refresh(db_feed)

    # Associate the feed with the user
    user_feed = UserFeedSchema(user_id= user.id, feed_id=db_feed.id)
    db.add(user_feed)
    db.commit()

    return {"message": "Feed added and scraped successfully", "feed_id": db_feed.id}
