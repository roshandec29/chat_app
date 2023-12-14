""" Model class for users """
import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr

from server.utils.common_utils import hash_user_ids


class User(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: str
    country_code: Optional[str] = "91"
    gender: Optional[int] = 1
    dob: Optional[str] = None
    status: Optional[int] = 1
    customer_category: Optional[int] = None
    updated_at: float = datetime.datetime.now().timestamp()
    is_active: bool = True
    is_deleted: bool = False

    def to_dict(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'updated_at': self.updated_at,
            'is_deleted': self.is_deleted,
            'is_active': self.is_active
        }


class UserCreate(User):
    pass

class UserList(User):
    _id: Optional[ObjectId] = None

    def to_dict(self):

        user_dict= {
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'updated_at': self.updated_at,
            'is_deleted': self.is_deleted,
            'is_active': self.is_active
        }
    
        if self.id:
            user_dict['_id'] = ObjectId(self.id)

        return user_dict