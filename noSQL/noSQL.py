from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection (adjust as per your local MongoDB setup)
client = MongoClient('mongodb://localhost:27017/')
db = client['local']  # The database name
collection = db['startup_log']  # The collection name

@app.route('/')
def index():
    # Fetch all documents from the startup_log collection
    data = list(collection.find({}))
    # Convert MongoDB documents to JSON-friendly format
    for doc in data:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string for HTML rendering

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)