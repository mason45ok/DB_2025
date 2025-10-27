from flask import Flask, request, render_template_string, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId # 用於處理 MongoDB 的 _id
import os
import logging
import json # 導入 json 模組來解析輸入的 JSON
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

# 假設這裡的密碼處理邏輯已在您的環境中解決
PASSWORD = os.getenv("PASSWORD", None)
if type(PASSWORD) != str:
    # 僅在環境變量未設置時打印警告，以允許代碼在沒有真實 MongoDB 連接的情況下運行
    #logging.warning(f"PASSWORD is : {PASSWORD} - 實際運行時需要有效的密碼")
    raise ValueError("密碼為空！！！")

# --- 1. 初始化 Flask 應用 ---
app = Flask(__name__)

# --- 2. 連接 MongoDB ---
# 確保您的 MongoDB 服務正在本機 (localhost) 的 27017 埠運行
# 否則請更改下方的連接字串
try:
    # 僅在 PASSWORD 存在時嘗試連接
    if PASSWORD:
        client = MongoClient(f'mongodb+srv://41171112h_db_user:{PASSWORD}@cluster0.r7apuot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        client.server_info() # 嘗試連接以觸發錯誤
        db = client['flask_demo_db'] # 選擇一個資料庫
        collection = db['users']      # 選擇一個集合 (collection)
        print("MongoDB 連接成功！")
    else:
        print("跳過 MongoDB 連接，因為缺少 PASSWORD。路由將無法工作。")
        collection = None # 設置為 None 以處理後續路由中的連接檢查
except Exception as e:
    print(f"無法連接到 MongoDB: {e}")
    collection = None
    pass


# --- 3. HTML 模板 ---
# 添加了一個新的表單來演示 insert_many 功能
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask & MongoDB Demo</title>
    <style>
        body { font-family: sans-serif; margin: 2em; }
        h1, h2 { color: #333; }
        form { margin-bottom: 2em; padding: 1em; background: #f4f4f4; border-radius: 5px; }
        ul { list-style: none; padding: 0; }
        li { margin: 0.5em 0; padding: 0.5em; background: #eee; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
        a { color: #d9534f; text-decoration: none; }
        a:hover { text-decoration: underline; }
        textarea { width: 100%; height: 100px; padding: 10px; box-sizing: border-box; }
        pre { background: #fff; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Flask + MongoDB Demo</h1>

    <h2>Add Single User (insert_one)</h2>
    <form action="/add" method="POST">
        name: <input type="text" name="name" required>
        age: <input type="number" name="age" required>
        <input type="submit" value="Add">
    </form>

    <hr>

    <h2>Add Multiple Users (insert_many)</h2>
    <form action="/add_many" method="POST">
        <label for="users_json">Enter Users as JSON Array:</label>
        <pre>[
  { "name": "Alice", "age": 25 },
  { "name": "Bob", "age": 30 }
]</pre>
        <textarea id="users_json" name="users_json" required></textarea><br>
        <input type="submit" value="Add Many">
    </form>

    <hr>

    <h2>user list</h2>
    <ul>
        {% for user in users %}
            <li>
                <span>ID: {{ user._id }} | name: {{ user.name }} | age: {{ user.age }}</span>
                <a href="/delete/{{ user._id }}">delete</a>
            </li>
        {% else %}
            <li>there's no user added</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# 檢查 MongoDB 連接的裝飾器 (Decorator)
def check_db_connection(f):
    """如果 collection 是 None，則重定向到主頁並顯示錯誤"""
    def decorated_function(*args, **kwargs):
        if collection is None:
            print("資料庫連接不可用，操作失敗。")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- 4. 定義路由 (Routes) ---

# (查看) 根目錄路由 - 顯示主頁面
@app.route('/')
def index():
    """
    這是主頁面，它會從 MongoDB 中 "查找" (find) 所有用戶，
    並將它們傳遞給 HTML 模板來顯示。
    """
    all_users = []
    if collection is not None:
        # .find() 會獲取集合中的所有文件
        all_users = list(collection.find())

    # 渲染我們定義的 HTML 模板，並傳入 users 變數
    return render_template_string(HTML_TEMPLATE, users=all_users)


# (新增) 創建新用戶的路由
@app.route('/add', methods=['POST'])
@check_db_connection
def add_user():
    """
    這個路由只接受 POST 請求 (來自 HTML 表單)。
    它會從表單中獲取數據，並 "插入" (insert_one) 一個新文件到 MongoDB。
    """
    # 已經由 @check_db_connection 檢查了 request.method 是 'POST'
    name = request.form['name']
    age = request.form['age']

    # 創建要插入的字典 (文件)
    new_user = {
        "name": name,
        "age": int(age) # 確保年齡是數字
    }

    # 將新用戶插入到集合中
    collection.insert_one(new_user)

    # 完成後，重定向回主頁面
    return redirect(url_for('index'))


# (批量新增) 批量創建新用戶的路由 (使用 insert_many)
@app.route('/add_many', methods=['POST'])
@check_db_connection
def add_many_users():
    """
    這個路由從表單中獲取一個 JSON 字串，解析它，並使用 insert_many 將多個文件插入到 MongoDB。
    """
    if request.method == 'POST':
        users_json_string = request.form['users_json']

        try:
            # 嘗試將字串解析為 Python 列表
            users_list = json.loads(users_json_string)

            if not isinstance(users_list, list):
                # 如果解析出來的不是列表，則報錯
                raise ValueError("JSON 格式不正確，預期為用戶物件的列表。")

            # 確保列表中的每個元素都是字典，並且有 'name' 和 'age'
            validated_users = []
            for user in users_list:
                if 'name' in user and 'age' in user:
                    # 確保 age 是整數
                    user['age'] = int(user['age'])
                    validated_users.append(user)
                else:
                    print(f"警告: 跳過無效的用戶物件: {user}")

            if validated_users:
                # 使用 insert_many 批量插入用戶列表
                result = collection.insert_many(validated_users)
                print(f"成功插入了 {len(result.inserted_ids)} 個用戶。")
            else:
                print("沒有有效的用戶可以插入。")

        except json.JSONDecodeError:
            print("錯誤：輸入的不是有效的 JSON 格式。")
        except ValueError as e:
            print(f"數據驗證錯誤: {e}")
        except Exception as e:
            print(f"插入多個用戶時出錯: {e}")

        # 完成後，重定向回主頁面
        return redirect(url_for('index'))


# (刪除) 刪除用戶的路由
@app.route('/delete/<id>')
@check_db_connection
def delete_user(id):
    """
    這個路由接受一個 URL 參數 'id'。
    它會使用這個 id 來 "刪除一個" (delete_one) 匹配的文件。
    """
    try:
        # MongoDB 的 _id 是 ObjectId 對象，不是簡單的字串
        # 所以我們需要從 'bson.objectid' 導入 ObjectId 來轉換它
        obj_id_to_delete = ObjectId(id)

        # 根據 _id 刪除文件
        result = collection.delete_one({"_id": obj_id_to_delete})

        if result.deleted_count == 0:
            print(f"警告：沒有找到 ID 為 {id} 的文件可刪除。")

    except Exception as e:
        print(f"刪除時出錯: {e}")

    # 完成後，重定向回主頁面
    return redirect(url_for('index'))


# --- 5. 運行應用 ---
if __name__ == '__main__':
    # debug=True 讓我們在開發時能看到錯誤，並在修改程式碼後自動重啟
    app.run(debug=True)