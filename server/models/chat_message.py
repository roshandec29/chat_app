"""
    Model class for chat messages
"""
import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MessageStatus(str, Enum):
    sent = 0
    received = 1
    read = 2


class ChatMessage(BaseModel):
    '''
        Chat message dataclass
    '''
    message: str
    message_id: str
    image_url: Optional[str] = None
    sender_id: str
    receiver_id: str
    conversation_id: str
    message_status: int = MessageStatus.sent
    updated_at: float
    is_deleted: bool = False

    def to_dict(self):
        return {
            'message': self.message,
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'image_url': self.image_url,
            'conversation_id': self.conversation_id,
            'message_status': self.message_status,
            'updated_at': self.updated_at,
            'is_deleted': self.is_deleted
        }