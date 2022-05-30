from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy.orm import as_declarative
from sqlalchemy.dialects.postgresql import UUID


@as_declarative()
class Base:
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
