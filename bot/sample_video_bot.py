from flask import Flask
from pyrogram import Client, filters
from bot.config import Config
from bot.messages import Messages
from bot.utils import Utilities
import logging
import threading
import os

logging.basicConfig(level=logging.DEBUG)

# Flask setup
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

# Pyrogram bot setup
class SampleVideoBot(Client):
    def __init__(self):
        super().__init__(
            "my_bot",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
        )

    async def start(self):
        await super().start()
        logging.info("Bot started")

    async def stop(self):
        await super().stop()
        logging.info("Bot stopped")

    @staticmethod
    async def handle_start_command(client, message):
        logging.info("Handling /start command")
        await message.reply_text("Welcome! Send a document to generate a sample video.")

    @staticmethod
    async def handle_sample_video(client, message):
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

bot_app = SampleVideoBot()

@bot_app.on_message(filters.command("start"))
async def start_command_handler(client, message):
    await SampleVideoBot.handle_start_command(client, message)

@bot_app.on_message(filters.document)
async def document_handler(client, message):
    await SampleVideoBot.handle_sample_video(client, message)

def run_bot():
    bot_app.run()

if __name__ == "__main__":
    # Start Flask server in a separate thread
    threading.Thread(target=run_flask).start()
    
    # Start Pyrogram bot
    run_bot()
