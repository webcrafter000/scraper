from flask import Flask, jsonify, render_template
import pymongo
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.ERROR)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["x_data"]
collection = db["trending_topics"]

# Flask app setup
absolute_template_path = r"D:\cdg_\working\scraping assignment task\templates"
app = Flask(__name__, template_folder=absolute_template_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trending', methods=['GET'])
def get_trending():
    try:
        record = collection.find().sort("timestamp", pymongo.DESCENDING).limit(1)
        trending_data = list(record)

        if trending_data:
            trending_topics = trending_data[0].get("trending_topics", [])
            return jsonify({"trending_topics": trending_topics})
        else:
            return jsonify({"error": "No trending topics found in the database"})
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return jsonify({"error": "Error fetching data from MongoDB", "details": str(e)})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(debug=True)
