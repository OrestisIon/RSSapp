from api import miniflux_manager as mdb
from api.models import Feed, Category, Icon, DiscoveredFeed, Entry
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from dependencies import get_authenticated_client
from miniflux import Client

feeds = APIRouter(dependencies = [Depends(get_authenticated_client)],
    responses={404: {"description": "Not found"}})
this_client: Client

@feeds.get('/', response_model=List[Feed])
async def index(request:Request):
    this_client = request.app.state.miniflux_client
    return await mdb.get_all_feeds(this_client)

@feeds.get('/{feed_id}', response_model=Feed)
async def index(request: Request,feed_id: int):
    this_client = request.app.state.miniflux_client
    return await mdb.get_feed(this_client, feed_id)

@feeds.get('/entries/{feed_id}', response_model=List[Entry])
async def index(request: Request, feed_id: int):
    this_client = request.app.state.miniflux_client
    return await mdb.get_feed_entries(this_client, feed_id)

@feeds.post('/', response_model=Feed)
async def create_feed(request: Request, url: str, category_id: int = None):
    this_client = request.app.state.miniflux_client
    return await mdb.create_feed(this_client, url, category_id)

@feeds.put('/{feed_id}', response_model=Feed)
async def update_feed(request: Request, feed_id: int, feed: Feed):
    this_client = request.app.state.miniflux_client
    return await mdb.update_feed(this_client, feed_id, feed)

@feeds.delete('/{feed_id}', response_model=Feed)
async def delete_feed(request: Request, feed_id: int):
    this_client = request.app.state.miniflux_client
    return await mdb.delete_feed(this_client, feed_id)

@feeds.get('/categories', response_model=List[Category])
async def get_all_categories(request: Request):
    this_client = request.app.state.miniflux_client
    return await mdb.get_all_categories(this_client)

@feeds.post('/categories', response_model=Category)
async def create_category(request: Request, title: str):
    this_client = request.app.state.miniflux_client
    return await mdb.create_category(this_client, title)

@feeds.get('/icons', response_model=List[Icon])
async def get_all_icons(request: Request):
    this_client = request.app.state.miniflux_client
    return await mdb.get_all_icons(this_client)

@feeds.get('/icons/{icon_id}', response_model=Icon)
async def get_icon(request: Request, icon_id: int):
    this_client = request.app.state.miniflux_client
    return await mdb.get_icon(this_client, icon_id)

@feeds.get('/categories/{category_id}', response_model=Category)
async def get_category(request: Request, category_id: int):
    this_client = request.app.state.miniflux_client
    return await mdb.get_category(this_client, category_id)

@feeds.post('/discover', response_model=List[DiscoveredFeed])
async def discover_feeds(request: Request, url: str):
    this_client = request.app.state.miniflux_client
    return await mdb.discover_feed(this_client, url)
