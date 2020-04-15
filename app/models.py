from app import db

from uuid import uuid4

class Choices(db.Model):
    __tablename__ = "choices"

    id = db.Column(
            "ID",
            db.Text(),
            default = lambda: str(uuid4()),
            primary_key = True,
            unique = True,
            nullable = False
            )
    session_data = db.Column(db.Text())

    def __repr__(self):
        return '<Choices {}>'.format(self.session_id)  