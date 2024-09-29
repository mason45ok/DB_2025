from flask import Blueprint, request, redirect, url_for
import mysql.connector

create_bp = Blueprint('create_bp', __name__)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'testdb'
}

@create_bp.route('/add', methods=['POST'])
def add_post():
    post_content = request.form['post']
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    insert_query = "INSERT INTO example_table (post) VALUES (%s)"
    cursor.execute(insert_query, (post_content,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('read_bp.index'))  # Redirect to the main view
