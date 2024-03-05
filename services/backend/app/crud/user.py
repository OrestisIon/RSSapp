from app.models import User as UserDBModel
from app.schemas.user import UserCreate 
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(db_session: AsyncSession, user_id: int):
    user = (await db_session.scalars(select(UserDBModel).where(UserDBModel.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(db_session: AsyncSession, email: str):
    statement = select(UserDBModel).where(UserDBModel.email == email)
    result = await db_session.execute(statement)
    user = result.scalars().first()
    return user


async def create_user(
    db_session: AsyncSession, 
    user: UserCreate
):
    userm = UserDBModel(
        username=user.username, 
        email=user.email, 
        first_name=user.first_name, 
        last_name=user.last_name, 
        hashed_password=pwd_context.hash(user.hashed_password), 
        is_superuser=user.is_superuser,
    )
    # Perform an action to validate the credentials, e.g., fetching the user's details
    # user_info = client.me()
    # feeds = client.get_feeds()
    # print(user_info)
    db_session.add(userm)
    await db_session.commit()
    # try:
    #     user = client.create_user(username=user.email, password=user.hashed_password, is_admin=False)
    # except miniflux.ClientError as e:
    #     # await db_session.rollback()
    #     raise HTTPException(status_code=400, detail=f"Error creating user in miniflux. Reason: {e}")
    # refresh the user to get the id
    await db_session.refresh(userm)
    return userm