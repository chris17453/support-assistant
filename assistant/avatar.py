import os
import uuid
from . import db

def list_cli():
    print("Avatar")
    db.list_cli(db.Avatar)



def insert(link_id, image_id, voice_id, name, description, style, speed=1, pitch=1,  active=True):
    # Create a new Avatar instance
    new_avatar = db.Avatar(
        name=name,
        description=description,
        image_id=image_id,
        voice_id=voice_id,
        style=style,
        speed=speed,
        pitch=pitch,
        uuid=str(uuid.uuid4()),
        link_id=link_id,
        active=active
    )

    # Insert the avatar into the database
    db.session.add(new_avatar)
    db.session.commit()

    print("Avatar created successfully.")

def get_by_id(id):
    record = db.session.query(db.Avatar).filter_by(id=id, active=True).first()
    return record

def get_by_link_id(link_id):
    records = db.session.query(db.Avatar).filter_by(link_id=link_id, active=True).all()
    return records

def get_by_uuid(uuid):
    record = db.session.query(db.Avatar).filter_by(uuid=uuid, active=True).first()
    return record


#def update_avatar(id, name, description, image_id, voice_id, style, speed, pitch, link_id, active):
#    avatar = session.query(Avatar).filter_by(id=id).first()
#    if avatar is None:
#        return None
#    else:
#        avatar.name = name
#        avatar.description = description
#        avatar.image_id = image_id
#        avatar.voice_id = voice_id """