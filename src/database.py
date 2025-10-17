from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import mapper_registry
from .settings import settings

engine = create_engine(settings.DATABASE_URL)
session = Session(engine)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def init_db():
    mapper_registry.metadata.drop_all(engine)
    mapper_registry.metadata.create_all(engine)
