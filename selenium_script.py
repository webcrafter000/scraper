import json
import time
from datetime import datetime
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import logging
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Twitter (X) credentials and MongoDB URI
X_USERNAME = os.getenv("X_USERNAME")
X_PASSWORD = os.getenv("X_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")

if not X_USERNAME or not X_PASSWORD or not MONGO_URI:
    logging.error("Missing environment variables: X_USERNAME, X_PASSWORD, or MONGO_URI")
    raise EnvironmentError("Check your .env file and environment variables.")

# MongoDB setup
client = pymongo.MongoClient(MONGO_URI)
db = client["x_data"]
collection = db["trending_topics"]

def get_public_ip():
    """Fetches the public IP address with a fallback."""
    try:
        ip_address = requests.get('https://api.ipify.org').text
        return ip_address
    except Exception as e:
        logging.error(f"Error fetching IP address: {e}")
        return "Unable to fetch IP address"

def get_trending_topics():
    logging.info("Initializing WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Use webdriver-manager to automatically handle ChromeDriver
    service = Service(ChromeDriverManager(driver_version="131.0.6778.205").install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open Twitter login page
        driver.get("https://x.com/i/flow/login")
        logging.info("Opening X login page...")

        # Login process
        username_field = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
        )
        username_field.send_keys(X_USERNAME)
        username_field.send_keys(Keys.RETURN)

        password_field = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(X_PASSWORD)
        password_field.send_keys(Keys.RETURN)

        # Fetch trending topics
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']//span"))
        )
        trends = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")

        # Extract and filter topics
        trending_topics = [
            trend.text.strip() for trend in trends
            if trend.text.strip() and trend.text.strip() not in ["What’s happening", "Trending in India", "LIVE"]
            and "Trending" not in trend.text and "posts" not in trend.text
        ]
        
        # Remove duplicates and limit to top 5 topics
        trending_topics = list(dict.fromkeys(trending_topics))[:5]

        # Get public IP address
        ip_address = get_public_ip()

        # Prepare the record
        record = {
            "unique_id": str(time.time()),
            "trending_topics": trending_topics,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip_address
        }

        # Print output
        logging.info(f"Inserting record into MongoDB: {record}")
        collection.insert_one(record)
        return json.dumps(record, indent=4)

    except Exception as e:
        logging.error(f"Error fetching trending topics: {e}")
        return json.dumps({"error": "Failed to fetch trending topics", "details": str(e)}, indent=4)

    finally:
        driver.quit()

if __name__ == "__main__":
    result = get_trending_topics()
    print(result)
