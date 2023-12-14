"""Module providing the MessagingData class to interact with the messaging controllers"""
import pymongo

from server.managers.mongo_db_manager import MongoDBConnection
from settings import get_settings
from server.models.user_model import User, UserList

from pymongo.collection import Collection
import re
settings = get_settings()


class UserData:
    """
        This class is responsible for User.
    """

    def __init__(self) -> None:
        """
            Initializes the messaging
        """
        self.client = MongoDBConnection().client
        self.data_base = self.client["chat"]
        self.user_collection: Collection[User] = self.data_base["user"]

    def add_user(self, user: User):
        """
            Adds a user
        """
        validated_phone_number = self.validate_phone_number(user.phone_number)

        if not validated_phone_number:
            return {"error": True, "data": {}, "message": "Invalid phone number"}

        # Check if the user already exists
        existing_user = self.user_collection.find_one({"phone_number": user.phone_number})
        
        if existing_user:
            existing_user["_id"] = str(existing_user["_id"])
            return {"error": False, "data": existing_user, "message": "User with the same phone number already exists"}


        try:
            # use pymongo to insert the message to the database
            # ensure document is updated if it already exists
            print("Adding user to the database")
            result = self.user_collection.insert_one(user.to_dict())
            # Fetch the inserted user with the retrieved ID
            inserted_user = self.user_collection.find_one({"_id": result.inserted_id})
            inserted_user["_id"] = str(result.inserted_id)

            return {"error": False, "data": inserted_user, "message": "User added successfully"}

        
        except Exception as error:
            print(f"Error adding user to the database: {error}")
            return {"error": True, "data": {}, "message": f"Error adding user to the database: {error}"}
            
    def get_all_users(self, page: int, limit: int, search: str = ""):
        """
        Gets all users with pagination and search
        """
        try:
            # Create a filter based on search criteria
            filter_criteria = {}  # You can customize this based on your search requirements
            if search:
                filter_criteria["$or"] = [
                    {"full_name": {"$regex": f".*{search}.*", "$options": "i"}},
                    # {"email": {"$regex": f".*{search}.*", "$options": "i"}},
                    # Add more fields as needed for search
                ]

            # use pymongo to get the users from the database with pagination and search
            users_cursor = (
                self.user_collection.find(filter_criteria)
                .sort([("updated_at", pymongo.DESCENDING)])
                .skip((page - 1) * limit)
                .limit(limit)
            )

            users=[]
            for user in users_cursor:
                user["_id"] = str(user["_id"])

                users.append(user)

            if not users:
                print("No users found in the database")
                return {"error": True, "data": [], "message": "No users found in the database"}

            return {"error": False, "data": users, "message": "Users found in the database"}

        except Exception as error:
            print(f"Error getting users from the database: {error}")
            return {"error": True, "data": [], "message": f"Error getting users from the database: {error}"}
        
    
    def validate_phone_number(self, phone_number):
        # Simple regex pattern for a generic phone number
        pattern = re.compile(r'^[6789]\d{9}$')
        print(pattern, phone_number)
        return bool(re.match(pattern, phone_number))

    
