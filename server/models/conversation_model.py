""" Model class for chat rooms """
import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from server.utils.common_utils import hash_user_ids


class ConversationBase(BaseModel):
    name: str
    description: str
    participants: list = []
    is_group: bool = False
    hashed_user_ids: Optional[str] = None
    updated_at: Optional[float] = None
    last_message: str = ""
    is_active: bool = False
    is_deleted: bool = False

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'participants': self.participants,
            'updated_at': self.updated_at,
            'hashed_user_ids': self.hashed_user_ids,
            'is_group': self.is_group,
            'last_message': self.last_message,
            'is_deleted': self.is_deleted,
            'is_active': self.is_active
        }


class ConversationList(ConversationBase):
    _id: Optional[ObjectId] = None

    def to_dict(self):

        return {
            '_id': str(self._id),
            'name': self.name,
            'description': self.description,
            'participants': self.participants,
            'updated_at': self.updated_at,
            'hashed_user_ids': self.hashed_user_ids,
            'is_group': self.is_group,
            'last_message': self.last_message,
            'is_deleted': self.is_deleted,
            'is_active': self.is_active
        }


class ConversationCreate(ConversationBase):
    pass


class UserConversationMap(BaseModel):

    user_id: str
    conversion_id: str
    updated_at: Optional[datetime.datetime] = None

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'conversion_id': self.conversion_id,
            'updated_at': self.updated_at
        }
