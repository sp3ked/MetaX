import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API constants
X_API_URL = "https://api.twitter.com/2/tweets"
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

def post_to_twitter(message):
    """Posts a given message to Twitter."""
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    payload = {"text": message}

    response = requests.post(X_API_URL, headers=headers, json=payload)

    if response.status_code == 201:
        print("Tweet posted successfully.")
    else:
        print(f"Failed to post tweet: {response.status_code}, {response.text}")

    return response.json()
