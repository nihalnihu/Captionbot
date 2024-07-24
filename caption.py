from pyrogram import Client, filters
from flask import Flask
import threading
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
bot = Flask(__name__)

@bot.route('/')
def hello_world():
    return 'Hello, World!'

@bot.route('/health')
def health_check():
    return 'Healthy', 200

def run_flask():
    bot.run(host='0.0.0.0', port=8080, use_reloader=False)

# Replace with your actual credentials
api_id = '25731065'
api_hash = 'be534fb5a5afd8c3308c9ca92afde672'
bot_token = '7213907869:AAGGYfN9m0OdUVtk-LzhEtyKJx3qVO8_DPI'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.video)
async def handle_video(client, message):
    logger.info(f"Received video from user {message.from_user.id}")
    await message.reply_text("Video received!")

async def main():
    # Start the Pyrogram Client
    await app.start()
    logger.info("Pyrogram client started")
    await asyncio.Event().wait()  # Keep the bot running

if __name__ == '__main__':
    # Start Flask in a separate thread
    threading.Thread(target=run_flask).start()

    # Run the Pyrogram client
    asyncio.run(main())
