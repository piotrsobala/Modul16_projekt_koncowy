# blog/models.py

from blog import db  # Import the initialized db instance from __init__.py


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Add pub_date field

    def __repr__(self):
        return f'<Entry {self.title}>'
