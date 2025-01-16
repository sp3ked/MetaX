from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from utils.whatsapp_utils import extract_last_message
from post_to_twitter import post_to_twitter
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
TARGET_CHAT = "Elon Musk (You)"  # Change this if needed

def main():
    # Initialize WebDriver
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver.get("https://web.whatsapp.com/")
    print("Scan the QR code to log in to WhatsApp Web.")
    time.sleep(15)  # Wait for manual login

    # Extract the last message
    last_message = extract_last_message(driver, TARGET_CHAT)
    if last_message:
        print(f"Extracted message: {last_message}")

        # Post to Twitter
        response = post_to_twitter(last_message)
        print("Posted to Twitter:", response)
    else:
        print("No message found.")

    driver.quit()

if __name__ == "__main__":
    main()
