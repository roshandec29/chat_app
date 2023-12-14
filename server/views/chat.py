import base64
import datetime
import uuid

from fastapi import WebSocket, WebSocketDisconnect, status, Response, APIRouter, UploadFile

from server.controllers.messaging_data import MessageData
from server.controllers.conversation_data import ConversationData
from server.controllers.user_data import UserData
from server.managers.imagekit_manager import ImageKitManager
from server.managers.messaging_manager import MessagingManager
from server.managers.conversation_manager import ConversationManager
from server.models.chat_message import ChatMessage, MessageStatus
from server.models.conversation_model import ConversationCreate
from server.models.user_model import User, UserCreate

chat_manager = MessagingManager()
conversation_manager = ConversationManager()


conversation_router = APIRouter()
conversation_ws_router = APIRouter()


@conversation_router.post("/add-conversation/", status_code=status.HTTP_201_CREATED)
async def handle_add_conversation(conversation: ConversationCreate, response: Response):
    """
        Function to handle new conversation created by a client
    """
    conversation_data = ConversationData()
    conversation, conversation_id = conversation_data.add_conversation(conversation)
    if conversation:
        await conversation_manager.broadcast_conversation(conversation)
        print(conversation, 'conversation details')
        return {"message": "conversation added", "data": {"conversation_id": conversation_id}}
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": "conversation not added"}


@conversation_router.get("/conversations/{user_id}", status_code=status.HTTP_200_OK)
async def handle_new_connection_conversation(user_id: str, response: Response):
    conversation_data = ConversationData()
    conversation = conversation_data.get_all_conversation(user_id)
    print(conversation, 'conversation details')
    return {"message": None, "data": {"conversation_list": conversation}}


@conversation_ws_router.websocket("/connect-conversation/{conversation_id}")
async def send_message(websocket: WebSocket, conversation_id: str):
    """
        Function to handle new connections to the conversation
        The function accepts the connection from the client
        and sends all the available conversation to the client
    """
    messages_data = MessageData()
    conversation_data = ConversationData()
    await chat_manager.connect(websocket, conversation_id)
    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_json()
            print(f"Received {data}")

            if "type" in data and data["type"] == "close":
                await chat_manager.disconnect(websocket, conversation_id)
            else:
                message = ChatMessage(
                    message_id=str(uuid.uuid4()),
                    sender_id=data["sender_id"],
                    receiver_id=data["receiver_id"],
                    message=data["message"],
                    image_url=data.get("image_url"),
                    conversation_id=conversation_id,
                    updated_at=datetime.datetime.now().timestamp()
                )
                messages_data.add_message(message)
                conversation_data.update_conversation(conversation_id, {'last_message': data["message"]})

                # Send the message to all the clients
                await chat_manager.broadcast(message, conversation_id)
    except WebSocketDisconnect:
        await chat_manager.disconnect(websocket, conversation_id)


@conversation_router.get("/get-messages/{conversation_id}", status_code=status.HTTP_200_OK)
async def handle_new_connection_conversation(conversation_id: str, response: Response):
    message_data = MessageData()
    messages = message_data.get_messages_of(conversation_id)
    print(messages, 'conversation details')
    return {"message": None, "data": {"message_list": messages}}


@conversation_router.post("/create-user/", status_code=status.HTTP_200_OK)
async def create_new_user(user: UserCreate, response: Response):
    user_data = UserData()
    user = user_data.add_user(user)
     
    if not user.get('error'):
        print(user, 'user details')
        return {"message": user.get('message'), "data": user.get('data')}
    
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": f"{user.get('message')}"}


@conversation_router.get("/user-list/", status_code=status.HTTP_200_OK)
async def get_all_user( response: Response, page: int = 1, limit: int = 10, search: str = ""):
    
    user_data = UserData()
    user = user_data.get_all_users(page=page, limit=limit, search=search)
     
    if not user.get('error'):
        print(user, 'user details')
        return {"message": user.get('message'), "data": user.get('data')}
    
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": f"{user.get('message')}"}


@conversation_router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile):
    binary_data = await file.read()
    base64_data = base64.b64encode(binary_data).decode('utf-8')
    image_url = ImageKitManager().upload_file(file, base64_data)
    return {"message": None, "data": {"image_url": image_url}}


@conversation_router.post("/receive-ack/", status_code=status.HTTP_200_OK)
async def received_ack(message_id: str, conversation_id: str):
    MessageData().update_message(message_id, {"message_status": MessageStatus.received})
    message = MessageData().get_message(message_id)
    await chat_manager.broadcast(message, conversation_id)
    return {"message": f"success"}


@conversation_router.post("/read-ack/", status_code=status.HTTP_200_OK)
async def read_ack(message_id: str, conversation_id: str):
    MessageData().update_message(message_id, {"message_status": MessageStatus.read})
    message = MessageData().get_message(message_id)
    await chat_manager.broadcast(message, conversation_id)
    return {"message": f"success"}
