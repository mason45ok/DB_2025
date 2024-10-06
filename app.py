from flask import Flask
from create import create_bp
from read import read_bp
from update import update_bp  # Import the update blueprint
from delete import delete_bp

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(create_bp)
app.register_blueprint(read_bp)
app.register_blueprint(update_bp)  # Register the update blueprint
app.register_blueprint(delete_bp)

if __name__ == '__main__':
    app.run(debug=True)
