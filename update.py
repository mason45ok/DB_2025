from flask import Blueprint, request, redirect, url_for
import mysql.connector

update_bp = Blueprint('update_bp', __name__)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'testdb'
}

@update_bp.route('/update/<int:post_id>', methods=['POST'])
def update_post(post_id):
    # 確保從表單中取得正確的值
    new_content = request.form.get(f'post_{post_id}')  # 使用 f-string 來根據 post_id 動態取得表單資料
    
    # 檢查是否有輸入資料，沒有的話返回錯誤
    if not new_content:
        return "No content to update", 400  # 返回 400 錯誤，告知無內容
    
    # 連接到資料庫並更新內容
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = "UPDATE example_table SET post = %s WHERE id = %s"
    
    # 執行更新語句
    cursor.execute(update_query, (new_content, post_id))
    conn.commit()  # 提交更改
    
    cursor.close()
    conn.close()
    
    # 更新完成後，重定向到主頁面
    return redirect(url_for('read_bp.index'))
