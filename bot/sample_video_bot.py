from flask import Flask, request, jsonify
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
from bot.config import Config
from bot.messages import Messages
from bot.utils import Utilities

# Initialize Flask app
app = Flask(__name__)

# Initialize Pyrogram bot
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

# Initialize the bot
bot = SampleVideoBot()

@app.route('/')
def home():
    return "Welcome to the Sample Video Bot API!"

@app.route('/start_bot', methods=['POST'])
def start_bot():
    """Start the bot."""
    try:
        threading.Thread(target=lambda: bot.run()).start()  # Start bot in a separate thread
        return jsonify({"status": "Bot started"}), 200
    except Exception as e:
        log.error(f"Error starting bot: {e}")
        return jsonify({"error": "Failed to start bot"}), 500

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    """Stop the bot."""
    try:
        bot.stop()  # Consider running this asynchronously if needed
        return jsonify({"status": "Bot stopped"}), 200
    except Exception as e:
        log.error(f"Error stopping bot: {e}")
        return jsonify({"error": "Failed to stop bot"}), 500

@app.route('/handle_sample_video', methods=['POST'])
def handle_sample_video():
    """Handle a sample video request."""
    data = request.json
    if 'file_id' in data:
        file_id = data['file_id']
        # Example response; you might want to process the file_id here
        return jsonify({"file_id": file_id, "message": "Sample video request received"}), 200
    else:
        return jsonify({"error": "Invalid request"}), 400

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # Start Flask in the main thread
    threading.Thread(target=run_flask).start()

    # Start the Pyrogram Client
    bot.run()
