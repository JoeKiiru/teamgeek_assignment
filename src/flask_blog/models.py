from datetime import datetime

from .database import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.relationship("Tag",  backref='posts', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return "<Post id={}, title='{}'>".format(self.id, self.title)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return "<Tag id={}, tag='{}'>".format(self.id, self.tag)
