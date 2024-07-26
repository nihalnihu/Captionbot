from flask import Flask, request, jsonify
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import signal
import sys
from bot.config import Config
from bot.messages import Messages
from bot.utils import Utilities

# Set up Flask app
flask_app = Flask(__name__)

# Set up Pyrogram bot
log = logging.getLogger(__name__)

class SampleVideoBot(Client):
    def __init__(self):
        super().__init__(
            "my_bot",  # Session name
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
        )

    async def start(self):
        await super().start()
        log.info("Bot started")

    async def stop(self):
        await super().stop()
        log.info("Bot stopped")

    @staticmethod
    async def handle_sample_video(client: Client, message: Message):
        if not message.document:
            await message.reply_text("Please send a document.")
            return

        file_id = message.document.file_id
        output_folder = "output"
        duration = Config.SAMPLE_VIDEO_DURATION

        await message.reply_text(Messages.SAMPLE_VIDEO_PROCESS_START)

        sample_video = await Utilities.generate_sample_video(file_id, output_folder, duration)

        if sample_video:
            await message.reply_document(sample_video, caption=Messages.SAMPLE_VIDEO_PROCESS_SUCCESS)
        else:
            await message.reply_text(Messages.SAMPLE_VIDEO_PROCESS_FAILED)

# Flask routes
@flask_app.route('/')
def home():
    return "Welcome to the Sample Video Bot API!"

@flask_app.route('/start_bot', methods=['POST'])
def start_bot():
    """Start the bot."""
    try:
        bot.loop.create_task(bot.start())  # Start the bot asynchronously
        return jsonify({"status": "Bot started"}), 200
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
        return jsonify({"error": "Failed to start bot"}), 500

@flask_app.route('/stop_bot', methods=['POST'])
def stop_bot():
    """Stop the bot."""
    try:
        bot.loop.create_task(bot.stop())  # Stop the bot asynchronously
        return jsonify({"status": "Bot stopped"}), 200
    except Exception as e:
        logging.error(f"Error stopping bot: {e}")
        return jsonify({"error": "Failed to stop bot"}), 500

@flask_app.route('/handle_sample_video', methods=['POST'])
def handle_sample_video():
    """Handle a sample video request."""
    data = request.json
    if 'file_id' in data:
        file_id = data['file_id']
        return jsonify({"file_id": file_id, "message": "Sample video request received"}), 200
    else:
        return jsonify({"error": "Invalid request"}), 400

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

def signal_handler(sig, frame):
    print('Signal received, shutting down...')
    bot.loop.create_task(bot.stop())  # Stop the bot gracefully
    sys.exit(0)

if __name__ == '__main__':
    bot = SampleVideoBot()
    
    # Add a handler to the bot
    bot.add_handler(filters.document & filters.private, SampleVideoBot.handle_sample_video)

    # Start the Flask app in a separate thread
    threading.Thread(target=run_flask).start()

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the Pyrogram bot
    bot.run()
