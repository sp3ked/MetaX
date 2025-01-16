from flask import Flask, request, jsonify
from post_to_twitter import post_to_twitter  # Import the Twitter posting function
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':  # Verification logic
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == os.getenv("VERIFICATION_TOKEN", "verify"):
            return challenge, 200
        else:
            return "Verification token mismatch", 403

    elif request.method == 'POST':  # Handle incoming messages
        try:
            data = request.get_json()
            print("Received data:", data)

            # Extract message text from WhatsApp payload
            if "messages" in data["entry"][0]["changes"][0]["value"]:
                message_data = data["entry"][0]["changes"][0]["value"]["messages"][0]
                text = message_data.get("text", {}).get("body", "No text found")
                print(f"Received WhatsApp message: {text}")

                # Post the message to Twitter
                response = post_to_twitter(text)
                print(f"Posted to Twitter: {response}")
                return jsonify({"status": "success", "twitter_response": response}), 200
            else:
                print("No messages found in webhook payload.")
                return jsonify({"status": "no_message"}), 200
        except Exception as e:
            print(f"Error handling webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
