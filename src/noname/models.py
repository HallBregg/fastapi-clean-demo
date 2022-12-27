from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger, DateTime, ForeignKey
from sqlalchemy.sql import func


metadata = MetaData()


link = Table(
  'link', metadata,
  Column('id', BigInteger, primary_key=True),
  Column('url', String),
  Column('created_at', DateTime, server_default=func.now())
)


tag = Table(
  'tag', metadata,
  Column('name', String, unique=True),
)


link_tag = Table(
  'link_tag', metadata,
  Column('link_id', ForeignKey('link.id')),
  Column('tag_name', ForeignKey('tag.name')),
)
