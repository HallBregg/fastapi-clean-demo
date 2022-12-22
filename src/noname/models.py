from sqlalchemy import Table, Column, Integer, String, MetaData


metadata = MetaData()


books = Table('book', metadata,
  Column('id', Integer, primary_key=True),
  Column('title', String),
  Column('primary_author', String),
)
