import os
import uuid
from . import db


def list_cli():
    print("Voices")
    # Retrieve all voices from the database
    db.list_cli(db.Voice)



def insert(link_id, account_id, name, description, gender, voice, active=True):
    # Create a new Voice instance
    new_voice = db.Voice(
        name=name,
        description=description,
        gender=gender,
        voice=voice,
        account_id=account_id,
        link_id=link_id,
        active=active
    )

    # Insert the voice into the database
    db.session.add(new_voice)
    db.session.commit()

    print("Voice created successfully.")


def get_by_id(id):
    record = db.session.query(db.Voice).filter_by(id=id, active=True).first()
    return record
    
