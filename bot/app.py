from flask import Flask, request, jsonify
import logging
from bot.sample_video_bot import SampleVideoBot

app = Flask(__name__)

# Initialize your bot
bot = SampleVideoBot()

@app.route('/')
def home():
    return "Welcome to the Sample Video Bot API!"

@app.route('/start_bot', methods=['POST'])
def start_bot():
    """Start the bot."""
    bot.start()
    return jsonify({"status": "Bot started"}), 200

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    """Stop the bot."""
    bot.stop()
    return jsonify({"status": "Bot stopped"}), 200

@app.route('/handle_sample_video', methods=['POST'])
def handle_sample_video():
    """Handle a sample video request."""
    data = request.json
    if 'file_id' in data:
        file_id = data['file_id']
        # Example response
        return jsonify({"file_id": file_id, "message": "Sample video request received"}), 200
    else:
        return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
