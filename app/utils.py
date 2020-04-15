import json
import base64
import uuid

from app import db
from app.models import Choices

from flask import session


def restore_session(session_id):
    """
    Retrieve session from db using base64 encoded uuid.
    """
    uuid = session_id_to_uuid(session_id)
    db_entry = Choices.query.get(uuid)
    old_session = json.loads(db_entry.session_data)

    session.update(old_session)
    session.modified = True


def add_new_session_to_db():
    """
    Create a new db entry using current session data. This entry is updated
    to contain the unique session id (base64 encoded uuid).
    """
    db_entry = Choices(session_data = session_json())

    db.session.add(db_entry)
    db.session.commit()

    uuid = db_entry.id # Must be after commit!
    session["session_id"] = uuid_to_session_id(uuid)
    update_session_in_db()


def update_session_in_db():
    """
    Update session db entry with current session info.
    """
    uuid = session_id_to_uuid(session.get("session_id"))
    db_entry = Choices.query.get(uuid)

    db_entry.session_data = session_json()
    db.session.commit()


def delete_session_from_db(session_id):
    """
    Delete db entry using session id.
    """
    uuid = session_id_to_uuid(session_id)
    db_entry = Choices.query.get(uuid)

    db.session.delete(db_entry)
    db.session.commit()


def initialise_session():
    """
    Set up session keys that are used by the app and create a db entry for the
    session.
    """
    session["choices"] = session.get("choices") or {}
    session["route"] = []
    session["current_page"] = "/"
    session.modified = True
    add_new_session_to_db()


def uuid_to_session_id(uuid_str):
    """
    Convert the UUID to a shorter session ID by base64 encoding.
    """
    return base64.urlsafe_b64encode(uuid.UUID(uuid_str).bytes).rstrip(b'=').decode('ascii')


def session_id_to_uuid(session_id):
    """
    Convert session ID to UUID by base64 decoding.
    """
    return str(uuid.UUID(bytes=base64.urlsafe_b64decode(session_id + '==')))

def session_json():
    """
    Convert session object to json, which can be stored in the db.
    """
    return json.dumps({key: value for key, value in session.items()})

