from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def extract_last_message(driver, chat_name):
    # Search for the chat
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.clear()
    search_box.send_keys(chat_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Extract the last message
    try:
        messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in span.selectable-text span")
        if messages:
            return messages[-1].text
        else:
            print("No messages found in chat.")
            return None
    except Exception as e:
        print(f"Error extracting messages: {e}")
        return None
