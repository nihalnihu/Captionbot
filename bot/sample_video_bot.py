from flask import Flask, request, jsonify
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import signal
import sys
from bot.web import keep_alive
from bot.config import Config
from bot.messages import Messages
from bot.utils import Utilities

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set up Pyrogram bot
log = logging.getLogger(__name__)

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

app = SampleVideoBot()
    
if __name__ == "__main__":
    keep_alive()
    app.run()
