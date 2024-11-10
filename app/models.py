import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, server_default='TRUE', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "published": self.published,
            "created_at": self.created_at
        }

    def __repr__(self):
        return json.dumps(self.to_dict())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at
        }

    def __repr__(self):
        return json.dumps(self.to_dict())