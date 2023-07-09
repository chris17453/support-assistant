import os
import uuid
from tabulate import tabulate
from . import db


def list_cli():
    print("Voices")
    # Retrieve all voices from the database
    voices = db.session.query(db.Voice).all()

    # Prepare voice data for tabular display
    voice_table = []
    for voice in voices:
        voice_table.append([voice.id, voice.account_id, voice.name, voice.description, voice.gender , voice.link_id, voice.active])

    # Define table headers
    headers = ['ID', 'Name', 'Description', 'Gender', 'Link ID', 'Active']

    # Display voices in tabular format
    print(tabulate(voice_table, headers, tablefmt='grid'))

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
    
