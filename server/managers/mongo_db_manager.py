import threading
from pymongo import MongoClient
from settings import get_settings


settings = get_settings()


class MongoDBConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(MongoDBConnection, cls).__new__(cls)
                cls._instance.client = None
                cls._instance.MONGODB_URI = settings.MONGODB_URI
                cls._instance.MAX_CONNECTIONS_COUNT = 10
                cls._instance.MIN_CONNECTIONS_COUNT = 1
        return cls._instance

    async def connect(self):
        with self._lock:
            if not self.client:
                self.client = MongoClient(
                    str(self.MONGODB_URI),
                    maxPoolSize=self.MAX_CONNECTIONS_COUNT,
                    minPoolSize=self.MIN_CONNECTIONS_COUNT,
                )
                print("Connected to MongoDB")

    async def close(self):
        with self._lock:
            if self.client:
                self.client.close()
                print("Closed MongoDB connection")


class MongoDB:
    connection: MongoDBConnection = None

    @classmethod
    async def get_connection(cls) -> MongoClient:
        if not cls.connection:
            cls.connection = MongoDBConnection()
            await cls.connection.connect()
        return cls.connection.client

    @classmethod
    async def close_connection(cls):
        if cls.connection:
            await cls.connection.close()
            cls.connection = None
