from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient, server_api
from bson.objectid import ObjectId  # Import ObjectId to handle MongoDB's default _id
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Function to connect to MongoDB
def connect_to_mongodb():
    mongo_username = quote_plus(os.getenv('MONGO_USERNAME'))
    db_password = quote_plus(os.getenv('MONGO_PASSWORD'))
    db_name = os.getenv('DB_NAME')

    # MongoDB connection URI
    uri = f"mongodb+srv://{mongo_username}:{db_password}@news-analyzer.0ittn.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=News-analyzer"
    client = MongoClient(uri, server_api=server_api.ServerApi('1'), ssl=True, tlsAllowInvalidCertificates=True)
    db = client[db_name]
    return db

# Route to fetch a single article by MongoDB _id
@app.route('/articles/<string:id>', methods=['GET'])    
def get_article_by_id(id):
    db = connect_to_mongodb()
    collection = db['PolarityData']
    
    try:
        # Convert string id to ObjectId
        article = collection.find_one({'_id': ObjectId(id)})
        
        if not article:
            return jsonify({"error": "Article not found"}), 404

        # Convert `_id` to string for frontend
        article['_id'] = str(article['_id'])
        return jsonify(article), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch all articles
@app.route('/articles', methods=['GET'])
def get_articles():
    db = connect_to_mongodb()
    collection = db['PolarityData']
    
    try:
        # Fetch all documents in the collection
        articles = list(collection.find({}))
        
        # Convert each `_id` to string for JSON serialization
        for article in articles:
            article['_id'] = str(article['_id'])

        return jsonify(articles), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
