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

logging.basicConfig(level=logging.DEBUG)

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

app = SampleVideoBot()

@app.on_message(filters.command("start"))
async def start_command_handler(client, message):
    await SampleVideoBot.handle_start_command(client, message)

if __name__ == "__main__":
    keep_alive()
    app.run()
