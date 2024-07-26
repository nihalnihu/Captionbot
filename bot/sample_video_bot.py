import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Config
from bot.messages import Messages
from bot.utils import Utilities

log = logging.getLogger(__name__)

class SampleVideoBot(Client):
    def __init__(self):
        super().__init__(
            session_name=Config.SESSION_NAME,
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
        )

    async def start(self):
        await super().start()
        print(f"Bot started")

    async def stop(self):
        await super().stop()
        print("Bot stopped")

    @staticmethod
    async def handle_sample_video(client: Client, message: Message):
        file_path = message.document.file_id  # Assuming the file is received as a document
        output_folder = "output"  # Folder where the sample video will be saved
        duration = Config.SAMPLE_VIDEO_DURATION

        await message.reply_text(Messages.SAMPLE_VIDEO_PROCESS_START)

        sample_video = await Utilities.generate_sample_video(file_path, output_folder, duration)

        if sample_video:
            await message.reply_document(sample_video, caption=Messages.SAMPLE_VIDEO_PROCESS_SUCCESS)
        else:
            await message.reply_text(Messages.SAMPLE_VIDEO_PROCESS_FAILED)

if __name__ == "__main__":
    bot = SampleVideoBot()
    bot.add_handler(filters.document & filters.private, SampleVideoBot.handle_sample_video)
    bot.run()
