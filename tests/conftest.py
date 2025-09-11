"""
Shared test fixtures and configuration
"""
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "hashed_password": "hashed_password",
        "body_type": "hourglass",
        "skin_tone": "warm",
        "style_preferences": {"style": "casual", "colors": ["blue", "green"]},
        "budget_range": "medium",
        "lifestyle": "professional",
        "sizing_info": {"top": "M", "bottom": "L"}
    }


@pytest.fixture
def sample_clothing_item_data():
    """Sample clothing item data for testing"""
    return {
        "user_id": 1,
        "description": "Blue cotton t-shirt",
        "category": "shirt",
        "colors": ["blue"],
        "fit_type": "regular",
        "formality_level": 2,
        "image_url": "https://example.com/image.jpg"
    }


@pytest.fixture
def sample_outfit_data():
    """Sample outfit data for testing"""
    return {
        "user_id": 1,
        "name": "Work Outfit",
        "clothing_items": [1, 2, 3],
        "description": "Professional look for office meetings",
        "user_rating": 5
    }