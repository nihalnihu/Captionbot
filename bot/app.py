from flask import Flask, request, jsonify
import logging
from bot.sample_video_bot import SampleVideoBot
import threading
import asyncio

app = Flask(__name__)

# Initialize your bot
bot = SampleVideoBot()

# Start the bot in a separate thread
def start_bot():
    asyncio.run(bot.start())

@app.route('/')
def home():
    return "Welcome to the Sample Video Bot API!"

@app.route('/start_bot', methods=['POST'])
def start_bot_route():
    """Start the bot."""
    try:
        threading.Thread(target=start_bot).start()
        return jsonify({"status": "Bot started"}), 200
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
        return jsonify({"error": "Failed to start bot"}), 500

@app.route('/stop_bot', methods=['POST'])
def stop_bot_route():
    """Stop the bot."""
    try:
        bot.stop()
        return jsonify({"status": "Bot stopped"}), 200
    except Exception as e:
        logging.error(f"Error stopping bot: {e}")
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
