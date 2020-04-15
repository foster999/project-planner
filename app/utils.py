import json
import base64
import uuid

from app import db
from app.models import Choices

from flask import session


def restore_session(session_id):
    uuid = session_id_to_uuid(session_id)
    db_entry = Choices.query.get(uuid)
    old_session = json.loads(db_entry.session_data)

    session.update(old_session)
    session.modified = True


def add_new_session_to_db():
    db_entry = Choices(session_data = session_json())

    db.session.add(db_entry)
    db.session.commit()

    uuid = db_entry.id # Must be after commit!
    session["session_id"] = uuid_to_session_id(uuid)
    update_session_in_db()


def update_session_in_db():
    uuid = session_id_to_uuid(session.get("session_id"))
    db_entry = Choices.query.get(uuid)

    db_entry.session_data = session_json()
    db.session.commit()


def delete_session_from_db(session_id):
    uuid = session_id_to_uuid(session_id)
    db_entry = Choices.query.get(uuid)

    db.session.delete(db_entry)
    db.session.commit()


def initialise_session():
    session["choices"] = session.get("choices") or {}
    session["route"] = []
    session["current_page"] = "/"
    session.modified = True
    add_new_session_to_db()


def uuid_to_session_id(uuid_str):
    return base64.urlsafe_b64encode(uuid.UUID(uuid_str).bytes).rstrip(b'=').decode('ascii')


def session_id_to_uuid(session_id):
    return str(uuid.UUID(bytes=base64.urlsafe_b64decode(session_id + '==')))

def session_json():
    return json.dumps({key: value for key, value in session.items()})

