from pyrogram import Client, filters
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import io
from flask import Flask
import logging
import threading

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
    bot.run(host='0.0.0.0', port=8080)
    

# Replace with your actual credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.video)
async def handle_video(client, message):
    # Download the video to memory
    video_stream = io.BytesIO()
    await message.download(video_stream)
    video_stream.seek(0)

    # Load the video into moviepy
    video_clip = VideoFileClip(io.BytesIO(video_stream.read()))

    # Create a text clip
    txt_clip = TextClip("Your Caption Here", fontsize=24, color='white', bg_color='black', size=video_clip.size)

    # Position the text at the top of the video
    txt_clip = txt_clip.set_position(('center', 'top')).set_duration(video_clip.duration)

    # Overlay the text on the video
    video_with_caption = CompositeVideoClip([video_clip, txt_clip])

    # Save the edited video to a BytesIO object
    output_video_stream = io.BytesIO()
    video_with_caption.write_videofile(output_video_stream, codec='libx264', audio_codec='aac', fps=24, threads=4, verbose=False)

    # Ensure we seek to the start of the BytesIO stream before sending
    output_video_stream.seek(0)

    # Send the edited video back
    await message.reply_video(output_video_stream, caption="Here is your video with the caption at the top.")

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    
    # Start the Pyrogram Client
    app.run()
