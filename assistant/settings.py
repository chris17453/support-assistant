import os



assets             = os.path.join( os.getcwd(),'assets' )
sessions_directory = os.path.join( os.getcwd(),'sessions')
database_file      = os.path.join( assets,'database','assistant.db')
persona_directory  = os.path.join( assets,'personas')
audio_directory    = os.path.join( assets,'audio')
video_directory    = os.path.join( assets,'video')
image_directory    = os.path.join( assets,'image')

from . import account
try:
    openai_api_secret  = account.get_by_name(name='OpenAI',link_id=1,).api_key
except:
    openai_api_secret  = None
    
