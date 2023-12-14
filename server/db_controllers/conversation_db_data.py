import datetime

import pymongo
from pymongo.collection import Collection

from server.managers.mongo_db_manager import MongoDBConnection
from server.models.conversation_model import ConversationCreate


class ConversationDBData:

    def __init__(self):
        # use pymongo to connect to the database
        self.client = MongoDBConnection().client
        self.data_base = self.client["chat"]
        self.conversion_collection: Collection[ConversationCreate] = self.data_base["conversation"]

    def update_single_conversation_doc(self, query, update):
        """
            Updates a single document in the database
        """
        try:
            update["$set"].update({"updated_at": datetime.datetime.utcnow()})
            result = self.conversion_collection.update_one(query, update, upsert=True)
            upserted_id = None
            # Check if a new document was inserted
            if result.upserted_id:
                upserted_id = result.upserted_id
            else:
                # No new document was inserted, you may want to query the document to get its _id
                existing_document = self.conversion_collection.find_one(query)
                if existing_document:
                    print(f"Document updated with _id: {existing_document['_id']}")
                    upserted_id = str(existing_document['_id'])
                else:
                    print("Error: Unable to find or insert document")
            print(result, 'result')
            return result, upserted_id
        except Exception as error:
            print(error)
            return None

    def filter_conversation(self, query):
        try:
            query.update({"is_deleted": False})
            result = self.conversion_collection.find(query).sort([('updated_at', pymongo.DESCENDING)])
            return result
        except Exception as error:
            print(error)
            return None