"""Module providing the conversationData class to interact with the conversation controllers"""
import datetime

from bson import ObjectId

from server.db_controllers.conversation_db_data import ConversationDBData
from server.db_controllers.user_conservation_db_data import UserConversationDBData
from server.models.conversation_model import ConversationCreate, UserConversationMap, ConversationList
from server.utils.common_utils import timestamp_to_date_format, hash_user_ids


class ConversationData:

    def __init__(self):
        # use pymongo to connect to the database
        self.conversation_db_inst = ConversationDBData()
        self.user_conv_db_inst = UserConversationDBData()

    def add_conversation(self, conversation: ConversationCreate):
        """
            Adds a conversation to the database
        """
        # use pymongo to insert the conversation to the database
        # ensure document is updated if it already exists
        print("Adding conversation to the database")
        try:
            conversation.hashed_user_ids = hash_user_ids(conversation.participants)
            valid_conversation = ConversationCreate(**conversation.to_dict())
            print(valid_conversation.to_dict(), 'valid conversation')
            if not valid_conversation:
                print(valid_conversation, "Invalid conversation")
                return None
            result, upserted_id = self.conversation_db_inst.update_single_conversation_doc(
                {"hashed_user_ids": valid_conversation.hashed_user_ids},
                {'$set': valid_conversation.to_dict()}
            )

            for participant in valid_conversation.participants:
                valid_user_conversation = UserConversationMap(
                    **{'user_id': participant, 'conversion_id': str(upserted_id), 'updated_at': datetime.datetime.utcnow()})
                result = self.user_conv_db_inst.update_single_doc(
                    {"conversion_id": valid_user_conversation.conversion_id, "user_id": valid_user_conversation.user_id},
                    {'$set': valid_user_conversation.to_dict()}
                )

            print("conversation added to the database")
            return valid_conversation, upserted_id
        except Exception as error:
            print(error)
            return None

    def update_conversation(self, conversation_id: str, payload: dict):
        """
            Updates a conversation to the database
        """
        # use pymongo to insert the conversation to the database
        # ensure document is updated if it already exists
        print("Updating conversation to the database")
        try:
            self.conversation_db_inst.update_single_conversation_doc(
                {"_id": ObjectId(conversation_id)},
                {'$set': payload}
            )
            print("conversation updated to the database")
        except Exception as error:
            print(error)
            return None

    def get_all_conversation(self, user_id: str):
        """
            Gets all conversation from the database
        """
        # use pymongo to get the conversation from the database
        try:
            result = []
            print("Getting all conversation from the database")
            # approach 1 where we can directly query the Conversation collection
            conversation_cursor = self.conversation_db_inst.filter_conversation({"participants": user_id})
            for conversation in conversation_cursor:
                conversation['_id'] = str(conversation['_id'])
                conversation['updated_at_str'] = conversation['updated_at'].strftime("%d %b %Y %H:%M")
                result.append(dict(conversation))
            return result
            # approach 2 where we can query the UserConversationMap collection
            # user_conversation_cursor = self.user_conv_db_inst.filter_with_lookup({"user_id": user_id})
            # return [Conversation(**conversation) for conversation in conversation_cursor]
        except Exception as error:
            print(error, 'error')
            return None
