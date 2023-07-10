import os
import uuid
from . import db


def list_cli():
    print("Utterance")
    # Fetch the avatars from the table
    db.list_cli(db.Utterance)



def insert(link_id, avatar_id=None, audio_id=None, video_id=None, text=None, count=None, variance=1, created=None, finished=None, processed=False, active=True):
    # Create a new Utterance instance
    new_utterance = db.Utterance(
        text=text,
        count=count,
        link_id=link_id,
        avatar_id=avatar_id,
        audio_id=audio_id,
        video_id=video_id,
        variance=variance,
        processed = processed,
        finished = finished,
        active=active
    )

    # Insert the utterance into the database
    db.session.add(new_utterance)
    db.session.commit()
    return new_utterance

    print("Utterance created successfully.")

def get_by_id(id):
    record = db.session.query(db.Utterance).filter_by(id=id, active=True).first()
    return record

def get_by_text_and_link(text,link_id,avatar_id):
    record = db.session.query(db.Utterance).filter_by(text=text,link_id=link_id,avatar_id=avatar_id,active=True).first()
    return record

def update_by_id(id, **kwargs):
    record = db.session.query(db.Utterance).filter_by(id=id, active=True).first()
    for key, value in kwargs.items():
        setattr(record, key, value)
    db.session.commit()
    return record