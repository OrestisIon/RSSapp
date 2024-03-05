### Backend - Database Migrations
#### In the root folder:
docker compose exec backend alembic revision --autogenerate -m "your message here" <br>
docker compose exec backend alembic upgrade head