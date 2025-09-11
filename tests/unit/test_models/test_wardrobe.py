"""
Unit tests for Wardrobe models (ClothingItem, Outfit, ShoppingRecommendation)
"""
import pytest
from app.models.wardrobe import ClothingItem, Outfit, ShoppingRecommendation


class TestClothingItemModel:
    """Test the ClothingItem model"""
    
    def test_clothing_item_creation(self, sample_clothing_item_data):
        """Test creating a clothing item"""
        item = ClothingItem(**sample_clothing_item_data)
        
        assert item.user_id == 1
        assert item.description == "Blue cotton t-shirt"
        assert item.category == "shirt"
        assert item.colors == ["blue"]
        assert item.fit_type == "regular"
        assert item.formality_level == 2
        assert item.image_url == "https://example.com/image.jpg"
    
    def test_clothing_item_defaults(self):
        """Test default values for clothing item"""
        item = ClothingItem(
            user_id=1,
            description="Basic shirt",
            category="shirt"
        )
        
        assert item.colors == []
        assert item.fit_type is None
        assert item.formality_level == 3  # Default formality level
        assert item.image_url is None
    
    def test_formality_level_range(self):
        """Test that formality level accepts valid range"""
        # Test valid formality levels
        for level in [1, 2, 3, 4, 5]:
            item = ClothingItem(
                user_id=1,
                description="Test item",
                category="shirt",
                formality_level=level
            )
            assert item.formality_level == level


class TestOutfitModel:
    """Test the Outfit model"""
    
    def test_outfit_creation(self, sample_outfit_data):
        """Test creating an outfit"""
        outfit = Outfit(**sample_outfit_data)
        
        assert outfit.user_id == 1
        assert outfit.name == "Work Outfit"
        assert outfit.clothing_items == [1, 2, 3]
        assert outfit.description == "Professional look for office meetings"
        assert outfit.user_rating == 5
    
    def test_outfit_optional_fields(self):
        """Test outfit with minimal required fields"""
        outfit = Outfit(
            user_id=1,
            clothing_items=[1, 2]
        )
        
        assert outfit.name is None
        assert outfit.description is None
        assert outfit.user_rating is None
        assert outfit.clothing_items == [1, 2]
    
    def test_outfit_clothing_items_relationship(self):
        """Test that outfits can reference multiple clothing items"""
        outfit = Outfit(
            user_id=1,
            clothing_items=[1, 2, 3, 4]
        )
        
        # Should store list of clothing item IDs
        assert len(outfit.clothing_items) == 4
        assert 1 in outfit.clothing_items
        assert 4 in outfit.clothing_items


class TestShoppingRecommendationModel:
    """Test the ShoppingRecommendation model"""
    
    def test_shopping_recommendation_creation(self):
        """Test creating a shopping recommendation"""
        recommendation = ShoppingRecommendation(
            user_id=1,
            item_type="blazer",
            description="Navy blue blazer for professional occasions",
            reasoning="Your wardrobe lacks formal outerwear for business meetings",
            priority_score=0.8,
            estimated_price_range="$100-200",
            complementary_items=[1, 3, 5]
        )
        
        assert recommendation.user_id == 1
        assert recommendation.item_type == "blazer"
        assert recommendation.description == "Navy blue blazer for professional occasions"
        assert recommendation.reasoning == "Your wardrobe lacks formal outerwear for business meetings"
        assert recommendation.priority_score == 0.8
        assert recommendation.estimated_price_range == "$100-200"
        assert recommendation.complementary_items == [1, 3, 5]
        assert recommendation.purchased is False  # Default value
    
    def test_shopping_recommendation_defaults(self):
        """Test default values for shopping recommendation"""
        recommendation = ShoppingRecommendation(
            user_id=1,
            item_type="shirt",
            description="White dress shirt",
            reasoning="Essential wardrobe staple",
            priority_score=0.5
        )
        
        assert recommendation.estimated_price_range is None
        assert recommendation.complementary_items == []
        assert recommendation.purchased is False
    
    def test_priority_score_range(self):
        """Test that priority score accepts valid range"""
        # Test valid priority scores
        for score in [0.0, 0.5, 1.0]:
            recommendation = ShoppingRecommendation(
                user_id=1,
                item_type="shirt",
                description="Test item",
                reasoning="Test reasoning",
                priority_score=score
            )
            assert recommendation.priority_score == score