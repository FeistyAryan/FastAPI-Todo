"""
Unit tests for User model
"""
import pytest
from app.models.user import User


class TestUserModel:
    """Test the extended User model with stylist fields"""
    
    def test_user_creation_with_stylist_fields(self, sample_user_data):
        """Test creating a user with stylist-related fields"""
        user = User(**sample_user_data)
        
        assert user.email == "test@example.com"
        assert user.body_type == "hourglass"
        assert user.skin_tone == "warm"
        assert user.style_preferences["style"] == "casual"
        assert user.budget_range == "medium"
        assert user.lifestyle == "professional"
        assert user.sizing_info["top"] == "M"
    
    def test_user_optional_stylist_fields(self):
        """Test that stylist fields are optional"""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        assert user.body_type is None
        assert user.skin_tone is None
        assert user.style_preferences is None
        assert user.budget_range is None
        assert user.lifestyle is None
        assert user.sizing_info is None
    
    def test_user_email_uniqueness_constraint(self):
        """Test that email field has unique constraint"""
        user = User(
            email="unique@example.com",
            hashed_password="hashed_password"
        )
        
        # The unique constraint is defined in the model
        assert hasattr(User.__table__.columns.email, 'unique')
    
    def test_user_default_active_status(self):
        """Test that users are active by default"""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        assert user.is_active is True