from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


class Info(db.Model):
    __tablename__ = 'info'

    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    smoke = db.Column(db.Integer, nullable=False)
    co = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'temp': self.temp,
            'humidity': self.humidity,
            'smoke': self.smoke,
            'co': self.co,
            'time': self.time.strftime("%m/%d/%Y, %H:%M:%S")
       }


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
