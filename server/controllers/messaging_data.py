"""Module providing the MessagingData class to interact with the messaging controllers"""
import datetime

import pymongo
from bson import ObjectId

from server.managers.mongo_db_manager import MongoDBConnection
from settings import get_settings
from server.models.chat_message import ChatMessage

from pymongo.collection import Collection

settings = get_settings()


class MessageData:
    """
        This class is responsible for storing messaging to the client.
    """

    def __init__(self) -> None:
        """
            Initializes the messaging
        """
        self.client = MongoDBConnection().client
        self.data_base = self.client["chat"]
        self.messages_collection: Collection[ChatMessage] = self.data_base["messages"]

    def add_message(self, message: ChatMessage):
        """
            Adds a message to the list
        """

        try:
            # use pymongo to insert the message to the database
            # ensure document is updated if it already exists
            print("Adding message to the database")
            self.messages_collection.insert_one(message.to_dict())
        except Exception as error:
            print(f"Error adding message to the database: {error}")

    def update_message(self, message_id: str, payload: dict):
        """
            Updates a conversation to the database
        """
        # use pymongo to insert the conversation to the database
        # ensure document is updated if it already exists
        print("Updating message to the database")
        update = {}
        try:
            update["$set"] = payload
            self.messages_collection.update_one({"message_id": message_id}, update, upsert=True)
            print("message updated to the database")
        except Exception as error:
            print(error)
            return None

    def get_messages_of(self, conversation_id: str):
        """
            Gets the messages of a specific conversation
        """
        try:
            # use pymongo to get the messages from the database
            print(
                f"Getting messages of {conversation_id} from the database")
            messages_cursor = self.messages_collection.find(
                {'conversation_id': conversation_id}).sort([('updated_at', pymongo.DESCENDING)])
            messages = [ChatMessage(**message) for message in messages_cursor]
            if len(messages) == 0:
                print(
                    f"No messages found for conversation {conversation_id} in the database")
            return messages
        except Exception as error:
            print(
                f"Error getting messages from the database: {error}")
            return []

    def get_message(self, message_id):
        """
        Retrieves a message from the database based on message_id
        """
        try:

            query = {"message_id": message_id}
            message_document = self.messages_collection.find_one(query)
            if message_document:
                message_document.pop('_id')
                message = ChatMessage(
                    message_id=message_document["message_id"],
                    sender_id=message_document["sender_id"],
                    receiver_id=message_document["receiver_id"],
                    message=message_document["message"],
                    image_url=message_document.get("image_url"),
                    conversation_id=message_document["conversation_id"],
                    updated_at=message_document["updated_at"],
                    is_deleted=message_document["is_deleted"],
                    message_status=message_document["message_status"]
                )
                return message
            else:
                print(f"Message with id {message_id} not found.")
                return None
        except Exception as error:
            print(f"Error retrieving message from the database: {error}")
            return None


