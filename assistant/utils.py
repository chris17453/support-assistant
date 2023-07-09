import os
import uuid
import argparse
import sqlite3
from tabulate import tabulate
from . import queue
from . import db
from . import owner
from . import link
from . import voice
from . import account
from . import image
from . import avatar
from . import utterance
from . import audio
from . import video
from . import process


#def delete_missing_files():
#    print("Cleaning up audio track rows where the file is missing")
#    conn = sqlite3.connect(config.DATABASE_FILE)
#    cursor = conn.cursor()
#
#    # Execute the query to fetch all rows from the audio table
#    cursor.execute("SELECT * FROM audio")
#    rows = cursor.fetchall()
#
#    deleted_rows = []
#
#    # Iterate over the rows and check if the corresponding file exists
#    for row in rows:
#        file_path = row[1]  # Assuming 'filename' is stored in the second column (index 1)
#        if not os.path.exists(file_path):
#            # File does not exist, delete the row from the database
#            cursor.execute("DELETE FROM audio WHERE id = ?", (row[0],))  # Assuming 'id' is stored in the first column (index 0)
#            deleted_rows.append(row)
#
#    # Commit the changes to the database
#    conn.commit()
#
#    # Close the database connection
#    cursor.close()
#    conn.close()
#
#
#    if len(deleted_rows) > 0:
#        print("Deleted rows:")
#        for row in deleted_rows:
#            print(row)
#    else:
#        print("No rows deleted.")
#
#
#def insert_audio_file(text):
#    audio.text_to_wav(config.DEFAULT_VOICE," ".join(text))
    

def insert_owner(args):
    owner.insert(args.name, args.description, args.active)

def insert_link(args):
    link.insert(args.owner_id,args.name, args.description, args.active)

def insert_voice(args):
    voice.insert(args.link_id, args.account_id, args.name, args.description,args.gender,args.voice,args.active)

def insert_image(args):
    image.insert(args.link_id,args.name, args.description, args.path, args.crop, args.active)

def insert_account(args):
    account.insert(args.link_id,args.name, args.description, args.endpoint, args.api_key, args.json, args.platform, args.active)

def insert_avatar(args):
    avatar.insert(args.link_id, args.image_id, args.voice_id, args.name, args.description, args.style, args.speed, args.pitch,  args.active)

def insert_utterance(args):
    utterance.insert(args.link_id, args.avatar_id, args.audio_id, args.video_id, args.text, args.count, args.variance, args.active)
      
def insert_video(args):
    video.insert(args.link_id, args.path, args.active)

def insert_audio(args):
    audio.insert(args.link_id, args.path, args.active)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assistant Utility")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
  
    db_parser = subparsers.add_parser('db', help='db utils')
    db_parser.add_argument("--init", action="store_true", help="Init the database")
    db_parser.add_argument("--describe", action="store_true",  help="show the table structure of the database")

# insert Owner
    owner_parser = subparsers.add_parser('insert_owner', help='insert an owner')
    owner_parser.add_argument('--name', required=True, help='Owner name')
    owner_parser.add_argument('--description', help='Owner description')
    owner_parser.add_argument('--active', action='store_true', help='Set owner as active')

    list_owner_parser     = subparsers.add_parser('list_owners', help='List all owners')
    list_link_parser      = subparsers.add_parser('list_links', help='List all links')
    list_voices_parser    = subparsers.add_parser('list_voices', help='List all voices')
    list_images_parser    = subparsers.add_parser('list_images', help='List all images')
    list_accounts_parser  = subparsers.add_parser('list_accounts', help='List all accounts')
    list_avatars_parser   = subparsers.add_parser('list_avatars', help='List all avatars')
    list_utterance_parser = subparsers.add_parser('list_utterances', help='List all utterances')
    list_video_parser     = subparsers.add_parser('list_videos', help='List all videos')
    list_audio_parser     = subparsers.add_parser('list_audio', help='List all audio files')


    # insert the parser for the "insert_link" command
    link_parser = subparsers.add_parser('insert_link', help='insert a link')
    link_parser.add_argument('--name', required=True, help='Link name')
    link_parser.add_argument('--description',  required=True, help='Description')
    link_parser.add_argument('--owner-id', type=int, required=True, help='Owner ID')
    link_parser.add_argument('--active', action='store_true', help='Set active')

    # insert the parser for the "insert_voice" command
    voice_parser = subparsers.add_parser('insert_voice', help='insert a voice')
    voice_parser.add_argument('--name', required=True, help='Link name')
    voice_parser.add_argument('--description',  required=True, help='Description')
    voice_parser.add_argument('--gender',  required=True, help='Sex')
    voice_parser.add_argument('--voice',  required=True, help='The actual voice value')
    voice_parser.add_argument('--account-id',  required=True, help='The account id to use google, elevenlabs, watson tts')
    voice_parser.add_argument('--link-id', type=int, required=True, help='Link ID')
    voice_parser.add_argument('--active', action='store_true', help='Set active')


    # insert the parser for the "insert_image" command
    image_parser = subparsers.add_parser('insert_image', help='insert an image')
    image_parser.add_argument('--name', required=True, help='Human name of the image')
    image_parser.add_argument('--description',  required=True, help='Description')
    image_parser.add_argument('--path',  required=True, help='The file location')
    image_parser.add_argument('--crop',  action="store_true", help='Crop the video to the face')
    image_parser.add_argument('--link-id', type=int, required=True, help='Link ID')
    image_parser.add_argument('--active', action='store_true', help='Set  active')

    # insert the parser for the "insert_account" command
    account_parser = subparsers.add_parser('insert_account', help='insert an service account')
    account_parser.add_argument('--name', required=True, help='Human name of the image')
    account_parser.add_argument('--description',  required=True, help='Description')
    account_parser.add_argument('--endpoint',   help='The url to connect to for this service')
    account_parser.add_argument('--api-key',   help='The secret token to login to the api')
    account_parser.add_argument('--json',   help='The json credential blob')
    account_parser.add_argument('--platform',  required=True, help='The provider, google, ibm, azure')
    account_parser.add_argument('--link-id',  type=int, help='Link ID')
    account_parser.add_argument('--active', action='store_true', help='Set active')


    # insert the parser for the "insert_avatar" command
    avatar_parser = subparsers.add_parser('insert_avatar', help='insert an avatar')
    avatar_parser.add_argument('--name', required=True, help='Link name')
    avatar_parser.add_argument('--description',  required=True, help='Description')
    avatar_parser.add_argument('--style',  required=True, help='style')
    avatar_parser.add_argument('--speed',  type=int, required=True, help='speed')
    avatar_parser.add_argument('--pitch',  type=int, required=True, help='pitch')
    avatar_parser.add_argument('--image-id',type=int, required=True, help='The image id')
    avatar_parser.add_argument('--voice-id',type=int, required=True, help='The voice id')
    avatar_parser.add_argument('--link-id', type=int, required=True, help='the link id')
    avatar_parser.add_argument('--active', action='store_true', help='Set active')



    # insert the parser for the "insert_utterance" command
    utterance_parser = subparsers.add_parser('insert_utterance', help='insert an utterance')
    utterance_parser.add_argument('--text',  required=True, help='the words spoken')
    utterance_parser.add_argument('--count',  type=int, required=True, help='the number of words')
    utterance_parser.add_argument('--variance',  type=int, required=True, help='version of the output')
    utterance_parser.add_argument('--avatar-id',type=int,required=True, default=None, help='The avatar to use for the video')
    utterance_parser.add_argument('--video-id',type=int, default=None, help='The video id')
    utterance_parser.add_argument('--audio-id',type=int, default=None, help='The audio id')
    utterance_parser.add_argument('--link-id', type=int, required=True, help='the link id')
    utterance_parser.add_argument('--active', action='store_true', help='Set active')


    # insert the parser for the "insert_video" command
    video_parser = subparsers.add_parser('insert_video', help='insert an video')
    video_parser.add_argument('--path',  required=True, help='the location of the video file')
    video_parser.add_argument('--link-id', type=int, required=True, help='the link id')
    video_parser.add_argument('--active', action='store_true', help='Set active')

    # insert the parser for the "insert_video" command
    audio_parser = subparsers.add_parser('insert_audio', help='insert audio')
    audio_parser.add_argument('--path',  required=True, help='the location of the video file')
    audio_parser.add_argument('--link-id', type=int, required=True, help='the link id')
    audio_parser.add_argument('--active', action='store_true', help='Set active')

    # create the parser for the "utterance" command
    process_parser = subparsers.add_parser('process', help='process an utterance')
    process_parser.add_argument('--avatar-id', type=int, required=True, help='the avatar to speak the text')
    process_parser.add_argument('--text'     ,  required=True, help='the text you want spoken')

    # create the parser for the "utterance" command
    process_batch_parser = subparsers.add_parser('process-batch', help='process an utterance batch')
    process_batch_parser.add_argument('--avatar-id', type=int, required=True, help='the avatar to speak the text')
    process_batch_parser.add_argument('--file'     ,  required=True, help='full with the text you want spoken')


    args = parser.parse_args()
    if  args.command == 'db':       
                    if args.init:
                            db.initialize_database()
                    if args.describe:
                            db.describe_database()

    elif args.command == 'insert_owner'    :
         insert_owner(args)
    elif args.command == 'insert_link'     :
         insert_link(args)
    elif args.command == 'insert_voice'    :
         insert_voice(args)
    elif args.command == 'insert_image'    :
         insert_image(args)
    elif args.command == 'insert_account'  :
         insert_account(args)
    elif args.command == 'insert_avatar'   :
         insert_avatar(args)
    elif args.command == 'insert_utterance':
         insert_utterance(args)
    elif args.command == 'insert_video'    :
         insert_video(args)
    elif args.command == 'insert_audio'    :
         insert_audio(args)
    elif args.command == 'list_owners'     :
         owner.list_cli()
    elif args.command == 'list_links'      :
         link.list_cli()
    elif args.command == 'list_voices'     :
         voice.list_cli()
    elif args.command == 'list_images'     :
         image.list_cli()
    elif args.command == 'list_accounts'   :
         account.list_cli()
    elif args.command == 'list_avatars'    :
         avatar.list_cli()
    elif args.command == 'list_utterances' :
         utterance.list_cli()
    elif args.command == 'list_audio'      :
         audio.list_cli()
    elif args.command == 'list_videos'     :
         video.list_cli()
    elif args.command == 'process'         :
         process.process(args.avatar_id,args.text)
    elif args.command == 'process-batch'   :
         process.process_batch(args.avatar_id,args.file)
    else :
        parser.print_help()
