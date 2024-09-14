from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'testdb'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_content = request.form['post']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        insert_query = "INSERT INTO example_table (post) VALUES (%s)"
        cursor.execute(insert_query, (post_content,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
