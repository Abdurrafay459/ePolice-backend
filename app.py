from flask import Flask
from db_config import configure_database, initialize_database

from incidents import incidents_blueprint

app = Flask(__name__)

app.register_blueprint(incidents_blueprint)

@app.route('/')
def home():
    return "Welcome to the ePolice Backend API!"

if __name__ == '__main__':
    app.run(debug=True)