import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base


@pytest.fixture(scope="function")
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    session = sessionmaker(bind=engine)()
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
