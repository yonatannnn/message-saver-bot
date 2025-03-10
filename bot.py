from telethon import TelegramClient, events
from pymongo import MongoClient
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
mongo_uri = os.getenv('MONGODB_URI')
target_user = os.getenv('TARGET_USER')

mongo_db_name = 'telegram_messages'
mongo_collection_name = 'messages'

mongo_client = MongoClient(mongo_uri)
db = mongo_client[mongo_db_name]
collection = db[mongo_collection_name]

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    sender = await event.get_sender()
    if sender.username == target_user or sender.id == target_user:
        print(f"New message from {sender.username}: {event.message.message}")

        message_data = {
            'sender_id': sender.id,
            'sender_username': sender.username,
            'message_text': event.message.message,
            'timestamp': event.message.date
        }
        collection.insert_one(message_data)
        print("Message saved to MongoDB!")

async def main():
    await client.start()
    print("Client started. Listening for new messages...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())