# FeedGpt

## Setup Guide
first time running: docker-compose up --build --no-recreate -d
then: docker-compose up -d

## DB Migrations
docker compose exec backend alembic revision --autogenerate -m "your message here"
docker compose exec backend alembic upgrade head

## URLs
### Miniflux
http://localhost:80/
### Backend 
http://localhost:8000/
### Client
http://localhost:3000/

