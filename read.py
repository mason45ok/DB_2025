from flask import Blueprint, render_template
import mysql.connector
# import traceback


read_bp = Blueprint('read_bp', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Mason45ok',
    'database': 'db_2025',
    #'ssl_disabled': True  
}

@read_bp.route('/')
def index():
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    select_query = "SELECT employee_name, employee_ID FROM employee"
    cursor.execute(select_query)
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # Render the posts with the add/delete functionality
    return render_template('index.html', posts=posts)
    


