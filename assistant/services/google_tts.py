from typing import Sequence
from google.oauth2 import service_account
import google.cloud.texttospeech as tts
import json
import re
import os
import uuid
import wave
import contextlib


def get_credentials(credentials):
    sa_credentials = service_account.Credentials.from_service_account_info(json.loads(credentials))
    return sa_credentials


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

def unique_languages_from_voices(voices: Sequence[tts.Voice]):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_languages(credentials):
    client = tts.TextToSpeechClient(credentials=credentials)
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

def text_to_wav(credentials,voice_name: str, text: str,path:str):
    sa_creds=get_credentials(credentials)
    #results=search_audio_by_text(text)
    #if results:
    #    print ("Text already generated")
    #    print(results)
    #    return
    
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient(credentials=sa_creds)
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    filename=os.path.join(path,generate_unique_filename()+".wav")
    word_count=count_words(text)
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
        with contextlib.closing(wave.open(filename,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        
    return {'filename':filename,'voice':voice_name,'duration':duration,'words':word_count,'text':text}

