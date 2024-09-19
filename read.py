from flask import Flask, render_template
import mysql.connector
from create import create_bp

app = Flask(__name__)
app.register_blueprint(create_bp)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'testdb'
}

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM example_table")
    tables = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', tables=tables)

if __name__ == '__main__':
    app.run(debug=True)
