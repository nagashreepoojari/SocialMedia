from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, server_default='TRUE', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'
