from flaskblog import db, login_manager
from datetime import datetime, timedelta
from flask import current_app
from flask_login import UserMixin
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        reset_token =jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.utcnow() + timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorcurrent_appithm="HS256"
        )
        return reset_token
    
    def verify_reset_token(token):
        try:
            payload = jwt.decode(
                    token,
                    current_app.config['SECRET_KEY'],
                    leeway=timedelta(seconds=10),
                    algorithms=["HS256"]
            )
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"