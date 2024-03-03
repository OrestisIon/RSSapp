from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Enum  # This is necessary for ENUM type
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import Table
from . import Base

user_feed_association = Table(
    'user_feed', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id'), primary_key=True)
)



# Define the ENUM type for category titles
category_titles = ('Sports', 'News', 'Technology', 'Entertainment', 'Lifestyle', 'Business', 'Science', 'Health', 'Education', 'Politics', 'Environment', 'Arts & Culture')

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    feeds: Mapped[list] = relationship("Feed", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(Enum(*category_titles, name="category_titles"))
    feeds: Mapped[list] = relationship("Feed", back_populates="category")

class Feed(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    feed_url: Mapped[str] = mapped_column(unique=True)
    text: Mapped[str]
    is_scrape: Mapped[bool]
    followers_counter: Mapped[int]
    category: Mapped[Category] = relationship("Category", back_populates="feeds")
