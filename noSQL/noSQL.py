from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於儲存 session 狀態

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['local']  # 替換為您的資料庫名稱
collection = db['startup_log']  # 替換為您的集合名稱

@app.route('/')
def index():
    # 預設不顯示全部資料
    show_all = session.get('show_all', False)
    data = list(collection.find({})) if show_all else []
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return render_template('index.html', data=data, results=None, show_all=show_all)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_doc = {'name': name, 'description': description}
        collection.insert_one(new_doc)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/search', methods=['POST'])
def search():
    query_text = str(request.form.get("query", ""))
    regex_query = {"$regex": query_text, "$options": "i"}
    query = {"$or": [{field: regex_query} for field in ["name", "description", "hostname", "startTime", "startTimeLocal", "pid"]]}

    results = list(collection.find(query))
    for result in results:
        result['_id'] = str(result['_id'])

    # 搜尋結果，不顯示全部資料
    return render_template('index.html', data=[], results=results, show_all=session.get('show_all', False))

@app.route('/show_all', methods=['GET'])
def show_all():
    # 切換顯示全部資料的狀態
    session['show_all'] = not session.get('show_all', False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
