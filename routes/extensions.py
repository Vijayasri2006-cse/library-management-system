import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lms_#@8389",
        database="library_db"
    )
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"