from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from . import Base

# Define the ENUM type for category titles
category_titles = ('General','Sports', 'News', 'Technology', 'Entertainment', 'Lifestyle', 'Business', 'Science', 'Health', 'Education', 'Politics', 'Environment', 'Arts & Culture')

# Association table for many-to-many relationship between User and Feed
user_feed_association = Table('user_feed', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('feed_id', Integer, ForeignKey('feeds.id'))
)

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)

    # Define the relationship to Feed
    feeds = relationship("Feed", secondary=user_feed_association, back_populates="users")

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(Enum(*category_titles, name="category_titles"))

    # Define the relationship to Feed
    feeds = relationship("Feed", back_populates="category")

class Feed(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    feed_url: Mapped[str] = mapped_column(unique=True)
    text: Mapped[str]
    is_scrape: Mapped[bool]
    followers_counter: Mapped[int]

    # Define the relationship to User
    users = relationship("User", secondary=user_feed_association, back_populates="feeds")

    # Foreign key for the one-to-many relationship with Category
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    # Define the relationship to Category
    category = relationship("Category", back_populates="feeds")