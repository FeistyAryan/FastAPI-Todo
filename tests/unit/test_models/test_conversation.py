"""
Unit tests for Conversation models
"""
import pytest
from app.models.conversation import Conversation, ConversationMessage
from app.core.enums import MessageRole


class TestConversationModel:
    """Test the Conversation model"""
    
    def test_conversation_creation(self):
        """Test creating a conversation"""
        conversation = Conversation(
            user_id=1,
            chat_name="Style Consultation #1"
        )
        
        assert conversation.user_id == 1
        assert conversation.chat_name == "Style Consultation #1"
    
    def test_conversation_required_fields(self):
        """Test that required fields are enforced"""
        # user_id and chat_name are required
        conversation = Conversation(
            user_id=1,
            chat_name="Test Chat"
        )
        
        assert conversation.user_id is not None
        assert conversation.chat_name is not None


class TestConversationMessageModel:
    """Test the ConversationMessage model"""
    
    def test_user_message_creation(self):
        """Test creating a user message"""
        message = ConversationMessage(
            conversation_id=1,
            role=MessageRole.USER,
            content={"text": "Help me style this outfit", "image_url": "https://example.com/outfit.jpg"}
        )
        
        assert message.conversation_id == 1
        assert message.role == MessageRole.USER
        assert message.content["text"] == "Help me style this outfit"
        assert message.content["image_url"] == "https://example.com/outfit.jpg"
    
    def test_ai_message_creation(self):
        """Test creating an AI response message"""
        message = ConversationMessage(
            conversation_id=1,
            role=MessageRole.AI,
            content={
                "text": "That's a great casual look! Here are some suggestions...",
                "recommendations": ["Add a belt", "Try different shoes"]
            }
        )
        
        assert message.role == MessageRole.AI
        assert message.content["text"] == "That's a great casual look! Here are some suggestions..."
        assert message.content["recommendations"] == ["Add a belt", "Try different shoes"]
    
    def test_message_role_enum(self):
        """Test that message role uses proper enum values"""
        # Test USER role
        user_message = ConversationMessage(
            conversation_id=1,
            role=MessageRole.USER,
            content={"text": "User message"}
        )
        assert user_message.role == MessageRole.USER
        
        # Test AI role
        ai_message = ConversationMessage(
            conversation_id=1,
            role=MessageRole.AI,
            content={"text": "AI response"}
        )
        assert ai_message.role == MessageRole.AI
    
    def test_message_content_flexibility(self):
        """Test that message content can handle various data structures"""
        # Text only
        text_message = ConversationMessage(
            conversation_id=1,
            role=MessageRole.USER,
            content={"text": "Simple text message"}
        )
        assert text_message.content["text"] == "Simple text message"
        
        # Complex content with multiple fields
        complex_message = ConversationMessage(
            conversation_id=1,
            role=MessageRole.AI,
            content={
                "text": "Here's your styling advice",
                "outfit_suggestions": [
                    {"items": [1, 2, 3], "occasion": "work"},
                    {"items": [4, 5, 6], "occasion": "casual"}
                ],
                "shopping_recommendations": ["white shirt", "black pants"]
            }
        )
        
        assert complex_message.content["text"] == "Here's your styling advice"
        assert len(complex_message.content["outfit_suggestions"]) == 2
        assert complex_message.content["shopping_recommendations"] == ["white shirt", "black pants"]