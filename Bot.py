from pyrogram import Client, filters
import asyncio
import aiohttp
from flask import Flask
import logging
import threading

# Replace these with your values
API_ID = '25731065'
API_HASH = 'be534fb5a5afd8c3308c9ca92afde672'
BOT_TOKEN = '7213907869:AAGGYfN9m0OdUVtk-LzhEtyKJx3qVO8_DPI'

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/health')
def health_check():
    return 'Healthy', 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Initialize Pyrogram Client
bot_client = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot_client.on_message(filters.photo | filters.video)
async def handle_media(client, message):
    file_id = message.photo.file_id if message.photo else message.video.file_id
    file_type = 'photo' if message.photo else 'video'
    
    # Generate a file thumbnail or screenshot
    await generate_preview(file_id, file_type)

async def generate_preview(file_id, file_type):
    # Get file info
    file_info = await bot_client.get_file(file_id)
    file_url = file_info.file_path
    
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status == 200:
                data = await resp.read()
                # Save or process the preview data
                preview_filename = f"preview.{file_type}"
                with open(preview_filename, "wb") as f:
                    f.write(data)
                logger.info(f"Preview saved as {preview_filename}")
            else:
                logger.error(f"Failed to download file: {resp.status}")

if __name__ == '__main__':
    # Start Flask in a separate thread
    threading.Thread(target=run_flask).start()
    
    # Start the Pyrogram Client
    bot_client.run()
