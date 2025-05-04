import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",passwd="")
from backend.utils.database import Database  # Update import
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id=None, username=None, email=None, password=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def create(username, email, password):
        db = Database()
        hashed_password = generate_password_hash(password)
        
        try:
            db.query(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def get_by_email(email):
        db = Database()
        try:
            result = db.query("SELECT * FROM users WHERE email = %s", (email,))
            user_data = result.fetchone()
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
            return None
        finally:
            db.close()

    def verify_password(self, password):
        return check_password_hash(self.password, password)