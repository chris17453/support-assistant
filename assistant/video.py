from sqlalchemy import create_engine, Column, Integer, String, desc, asc, func
import os
import uuid
import subprocess
import json
from tabulate import tabulate
from . import db

def list_cli():
    print("Video")
    # Fetch the avatars from the table
    
    data = db.session.query(db.Video).all()
    if len(data) == 0:
        print("No data found.")
        return
    headers = data[0].__table__.columns.keys()
    rows = [[getattr(obj, column) for column in headers] for obj in data]
    print(tabulate(rows, headers=headers))



def get_video_length(filepath):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', filepath]
    result = subprocess.run(command, capture_output=True, text=True)
    print(" ".join(command))

    if result.returncode == 0:
        output = json.loads(result.stdout.strip())
        duration = float(output['format']['duration'])
        return duration
    else:
        print('Error:', result.stderr)


def insert(link_id, path, dub=False, active=True):
    # Create a new Video instance
    base_dir = os.path.dirname(path)
    filename = os.path.basename(path)
    length=get_video_length(path)
    print ("length: {0}".format(length))
    
    record = db.Video(
        name=filename,
        path=base_dir,
        length=length,
        dub=dub,
        link_id=link_id,
        uuid=str(uuid.uuid4()),
        active=active
    )

    # Insert the video into the database
    db.session.add(record)
    db.session.commit()


    print("Video created successfully.")
    return record

def update_by_id(id, **kwargs):
    record = db.session.query(db.Video).filter_by(id=id, active=True).first()
    for key, value in kwargs.items():
        setattr(record, key, value)
    db.session.commit()
    return record

def get_by_id(id):
    record = db.session.query(db.Video).filter_by(id=id, active=True).first()
    return record

def get_by_uuid(uuid):
    record = db.session.query(db.Video).filter_by(uuid=uuid, active=True).first()
    return record


def get_by_length(link_id,avatar_id,length):
    print ("Searching for video with length {0}".format(length))
    record = db.session.query(db.Video).filter_by(length>length, link_id=link_id, avatar_id=avatar_id, active=True).order_by(asc(db.Video.length)).first()
    return record

def get_closest_videos_by_length(avatar_id, link_id, target_length):
    print("X{0} Y{1} Z{2} ".format(avatar_id, link_id, target_length))
    record = db.session.query(db.Video)\
        .join(db.Utterance, db.Utterance.video_id == db.Video.id)\
        .filter(db.Utterance.avatar_id == avatar_id)\
        .filter(db.Utterance.link_id == link_id)\
        .filter(db.Video.length >= target_length, db.Video.active == True, db.Utterance.active == True)\
        .order_by(db.Video.length)\
        .first()

    print(record)
    return record