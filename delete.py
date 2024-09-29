from flask import Blueprint, request, redirect, url_for
import mysql.connector

delete_bp = Blueprint('delete_bp', __name__)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'testdb'
}

@delete_bp.route('/delete', methods=['POST'])
def delete_posts():
    selected_ids = request.form.getlist('post_ids')
    
    if selected_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        delete_query = "DELETE FROM example_table WHERE id IN (%s)" % ','.join(['%s'] * len(selected_ids))
        cursor.execute(delete_query, tuple(selected_ids))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    return redirect(url_for('read_bp.index'))  # Redirect to the main view
