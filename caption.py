from pyrogram import Client, filters
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import tempfile
import logging
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
    try:
        # Download the video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
            await message.download(temp_input.name)
            temp_input.seek(0)

            # Load the video into moviepy
            video_clip = VideoFileClip(temp_input.name)

            # Create a text clip
            txt_clip = TextClip("Your Caption Here", fontsize=24, color='white', bg_color='black', size=video_clip.size)

            # Position the text at the top of the video
            txt_clip = txt_clip.set_position(('center', 'top')).set_duration(video_clip.duration)

            # Overlay the text on the video
            video_with_caption = CompositeVideoClip([video_clip, txt_clip])

            # Save the edited video to another temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
                video_with_caption.write_videofile(temp_output.name, codec='libx264', audio_codec='aac', fps=24, threads=4, verbose=False)
                temp_output.seek(0)

                # Send the edited video back
                await message.reply_video(temp_output.name, caption="Here is your video with the caption at the top.")
                
    except Exception as e:
        logger.error(f"Error processing video: {e}")

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
