from flask import Flask, request, jsonify
from post_to_twitter import post_to_twitter
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    try:
        # Get the JSON payload from WhatsApp
        data = request.get_json()

        # Extract the message text from the payload
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            text = message.get("text", {}).get("body", "No text found")
            print(f"Received WhatsApp message: {text}")

            # Post the message to Twitter
            response = post_to_twitter(text)
            return jsonify({"status": "success", "twitter_response": response}), 200
        else:
            print("No message content found in payload.")
            return jsonify({"status": "no_message"}), 200
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
