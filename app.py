from flask import Flask
from create import create_bp  # Use create_bp from create.py
from read import read_bp
from delete import delete_bp

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(create_bp)  # Register create_bp
app.register_blueprint(read_bp)
app.register_blueprint(delete_bp)

if __name__ == '__main__':
    app.run(debug=True)
