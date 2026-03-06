from flask import Flask
from flask import Flask, render_template
from flask_login import LoginManager
from models.ModelUser import ModelUser
from extensions import db

from routes.auth import auth
from routes.dashboard import dashboard
from routes.propietarios import propietarios
from routes.admin import admin

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("pagina/index.html")

# CONFIG MYSQL desde .env
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT')) 

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

print(os.getenv('MYSQL_USER'))
print(os.getenv('MYSQL_PORT'))

print("MYSQL_USER:", os.getenv("MYSQL_USER"))
print("MYSQL_PASSWORD:", os.getenv("MYSQL_PASSWORD"))
print("MYSQL_PORT:", os.getenv("MYSQL_PORT"))

# init db
db.init_app(app)

# login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(propietarios, url_prefix='/propietarios')
app.register_blueprint(admin)

if __name__ == '__main__':
    app.run(debug=True)



