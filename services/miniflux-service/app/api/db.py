
from sqlalchemy import (Column, Integer, MetaData, String, Text, Table,
                        create_engine, ARRAY)
from databases import Database
import os
from sqlalchemy import CheckConstraint

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('email', String(50)),
    Column('country', String(50), nullable=True),
    Column('age', Integer, CheckConstraint('age < 100')),
    Column('password', String(50))
)

# create feeds table
feeds = Table(
    'feeds',
    metadata,
    Column('feed_url', String(100), primary_key=True),
    Column('site_url', String(50)),
    Column('category', String(50)),
    Column('text_for_embedding', Text()),
    Column('icon', String(50))
)
# Categories Table
# There is a predefined category table in the database
# The category table is used to group feeds
# Each user can have multiple categories
# Some categories are predefined and cannot be deleted
# The predefined categories are:
# All Feeds
# Starred
# Published
# Archived
# Read Later
# Labels
# The user can create custom categories
# The user can rename and delete custom categories
# The user can assign a color to a custom category
# The user can assign a category to a feed
categories = Table(
    'categories',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('title', String(50)),
    Column('order_id', Integer),
    Column('collapsed', Integer),
    Column('color', String(50)),
    Column('created_at', String(50)),
    Column('updated_at', String(50)),
    Column('user', String(50)),
    Column('feed_ids', ARRAY(Integer))
)

database = Database(DATABASE_URI)