import pymongo
from pymongo.collection import Collection

from server.managers.mongo_db_manager import MongoDBConnection
from server.models.conversation_model import ConversationCreate


class UserConversationDBData:

    def __init__(self):
        # use pymongo to connect to the database
        self.client = MongoDBConnection().client
        self.data_base = self.client["chat"]
        self.user_conversion_collection: Collection[ConversationCreate] = self.data_base["user_conversation_map"]

    def update_single_doc(self, query, update):
        """
            Updates a single document in the database
        """
        try:
            result = self.user_conversion_collection.update_one(query, update, upsert=True)
            upserted_id = None
            # Check if a new document was inserted
            if result.upserted_id:
                upserted_id = result.upserted_id
            else:
                # No new document was inserted, you may want to query the document to get its _id
                existing_document = self.user_conversion_collection.find_one(query)
                if existing_document:
                    print(f"Document updated with _id: {existing_document['_id']}")
                    upserted_id = str(existing_document['_id'])
                else:
                    print("Error: Unable to find or insert document")
            return result, upserted_id
        except Exception as error:
            print(error)
            return None

    def filter(self, query):
        try:
            query.update({"is_deleted": False})
            result = self.user_conversion_collection.find(query).sort([('updated_at', pymongo.DESCENDING)])
            return result
        except Exception as error:
            print(error)
            return None

    def filter_with_lookup(self, query):
        """
            This method is used to get the conversations with the latest message
        """
        result = self.user_conversion_collection.aggregate([
            {"$match": query},
            {"$lookup": {
                "from": "conversations",
                "localField": "conversation_id",
                "foreignField": "_id",
                "as": "conversation"
            }},
            {"$unwind": "$conversation"},
            {"$sort": {"conversation.updated_at": -1}},
            {"$limit": 10}  # Adjust as needed
        ])
        return result