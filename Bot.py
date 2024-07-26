from pyrogram import Client, filters
import asyncio
import aiohttp

# Replace these with your values
API_ID = '25731065'
API_HASH = 'be534fb5a5afd8c3308c9ca92afde672'
BOT_TOKEN = '7213907869:AAGGYfN9m0OdUVtk-LzhEtyKJx3qVO8_DPI'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.photo | filters.video)
async def handle_media(client, message):
    # Check if the message contains a photo or video
    if message.photo:
        file_id = message.photo.file_id
        file_type = 'photo'
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
    else:
        return

    # Generate a file thumbnail or screenshot
    await generate_preview(file_id, file_type)

async def generate_preview(file_id, file_type):
    # Use Telegram API to get the file
    file = await app.get_media(file_id)
    file_url = file.file_path

    # Download a preview (mock-up; implement actual preview generation logic)
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status == 200:
                data = await resp.read()
                # Save or process the preview data
                # For example, save to a local file
                with open(f"preview.{file_type}", "wb") as f:
                    f.write(data)
            else:
                print(f"Failed to download file: {resp.status}")

app.run()
