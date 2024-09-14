from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'employeesystem'
}

@app.route('/')
def show_employees():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Execute the query
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Render the data in an HTML template
    return render_template('employees.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
