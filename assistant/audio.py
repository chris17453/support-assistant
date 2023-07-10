import re
import uuid
import os
import subprocess
import json
import uuid
from . import settings
from . import db
from .services import google_tts



def list_cli():
    print("Audio")
    db.list_cli(db.Audio)



def watson_text_to_Wav(voicename, text):
    from ibm_watson import TextToSpeechV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    authenticator = IAMAuthenticator('api_key')
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url('service_url')

    sample = "insert what you want to say here"

    with open('test.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                sample,
                voice='en-GB_JamesV3Voice',
                accept='audio/wav'
            ).get_result().content)
    




def generate_unique_filename():
    unique_id = uuid.uuid4()
    filename = str(unique_id)
    return filename

def count_words(text):
    # Remove punctuation from the text using regular expressions
    text = re.sub(r'[^\w\s]', '', text)
    
    # Split the text into words and count them
    words = text.split()
    word_count = len(words)
    
    return word_count


def get_audio_length(filepath):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', filepath]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        output = json.loads(result.stdout)
        duration = float(output['format']['duration'])
        return duration
    else:
        print('Error:', result.stderr)

def insert(link_id, path, active=True):
    # Create a new Video instance
    base_dir = os.path.dirname(path)
    filename = os.path.basename(path)
    length=get_audio_length(path)

    # Create a new Audio instance
    new_audio = db.Audio(
        name=filename,
        path=base_dir,
        length=length,
        uuid=str(uuid.uuid4()),
        link_id=link_id,
        active=active
    )

    # Insert the audio into the database
    db.session.add(new_audio)
    db.session.commit()
    print("Audio created successfully.")
    return new_audio


def get_by_id(id):
    record = db.session.query(db.Audio).filter_by(id=id, active=True).first()
    return record

def get_by_uuid(uuid):
    record = db.session.query(db.Audio).filter_by(uuid=uuid, active=True).first()
    return record

def create(account,voice, text,path):
    results=None
    print("Creating audio for {0} at {1} using {2}".format(account.platform,path,voice.voice))
    print(account.platform)
    if account.platform.lower()=="google":
        credentials=account.json
        results=google_tts.text_to_wav(credentials,voice.voice, text,path)

    return results
