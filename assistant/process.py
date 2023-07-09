import os
import uuid
import subprocess
from datetime import datetime
from . import audio
from . import video
from . import image
from . import voice
from . import utterance
from . import avatar
from . import account
from . import db
from . import settings


# this class builds a video and audio file from a text utterance
#  in real time it does not build videos because it takes too long
#  it does generate audio in real time
#  existing silent video files with the correct links and word count or dubbed with the correct audio
#  batch files run in the evening audio that needs video
class utterance_builder:
    def __init__(self,avatar_id,text,realtime=False):
        self.audio_results=None
        self.finished=None
        self.avatar_id=avatar_id
        self.text=text
        self.realtime=realtime
        self.load_deps()
        
        
        self.utterance=utterance.get_by_text_and_link(text,self.avatar.link_id)

        # if this is an already built utterance, it needs a video
        if self.utterance:
            self.build_video_for_existing()
        else:
        ## otherwise this is a new utterance and needs audio and video
            self.build_new_utterance()
        

    def build_video_for_existing(self):
        print("Utterance already exists")
        if self.utterance.audio_id==None:
            print("Audio does not exist")
        else:
            self.audio=audio.get_by_id(self.utterance.audio_id)
            print("Loaded Audio")


        if self.utterance.video_id:
            self.video=video.get_by_id(self.utterance.video_id)
            print("Video exist for utterance,aborting")
            return
        
        if self.realtime==False:
            self.generate_cmd()
            self.video=video.insert(self.avatar.link_id, self.video_file, active=True)
            self.utterance.video_id=self.video.id
            db.session.commit()
        else:
            self.dub_video()
            self.video=video.insert(self.avatar.link_id, self.video_file,dub=True, active=True)
            self.utterance=utterance.insert(self.avatar.link_id, avatar_id=self.avatar_id,audio_id=self.audio.id,video_id=self.video.id, text=self.text, count=count, variance=1, created=self.created, finished=self.finished, processed=True, active=True)
    
    def build_new_utterance(self):
        print("Utterance does not exist")
        self.created=datetime.now()
        #self.debug()
        count=audio.count_words(self.text)
        x=None
        self.audio_results=audio.create(self.account,self.voice,self.text,settings.audio_directory)
        print("---***** In UTTERANCE BUILDER")
        if self.audio_results:
            path=self.audio_results['filename']
            print("New audio created")
            self.audio=audio.insert(self.avatar.link_id, path, active=True)
            if self.realtime==False:
                print ("Real")
                self.generate_cmd()
                self.finished=datetime.now()
                self.video=video.insert(self.avatar.link_id, self.video_file, active=True)
                self.utterance=utterance.insert(self.avatar.link_id, avatar_id=self.avatar_id,audio_id=self.audio.id,video_id=self.video.id, text=self.text, count=count, variance=1, created=self.created, finished=self.finished, processed=True, active=True)
            else:
                print ("Dub")
                self.dub_video()
                self.finished=datetime.now()
                self.video=video.insert(self.avatar.link_id, self.video_file,dub=True, active=True)
                self.utterance=utterance.insert(self.avatar.link_id, avatar_id=self.avatar_id,audio_id=self.audio.id,video_id=self.video.id, text=self.text, count=count, variance=1, created=self.created, finished=self.finished, processed=True, active=True)
        

    def generate_cmd(self):    
        
        audio_file=self.audio.path+"/"+self.audio.name
        image_file=self.image.image_path+"/"+self.image.image_name
        
        print("Building Video")
        cmd=["cd /home/nd/ai/SadTalker;"
        "/home/nd/ai/SadTalker/venv/bin/python /home/nd/ai/SadTalker/inference.py "+
        "--driven_audio '{0}' ".format(audio_file)+
        "--source_image '{0}' ".format(image_file)+
        "--result_dir {0} ".format(settings.video_directory)+
        "--still "+
        "--preprocess full "+
        "--enhancer gfpgan "]
        
        # Open the subprocess and wait for it to complete
        process = subprocess.Popen(cmd,shell=True , stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        #process.wait()
        output, error = process.communicate()

        output = output.decode("utf-8").strip()
        file=output.split("\n")[-1]
        file=file.split("named:")[1]
        file=file.strip()
        self.video_file=file

        print("video file: {0}".format(self.video_file))


        # The subprocess has completed
        print("Subprocess completed with return code:", process.returncode)
        #print(" ".join(cmd))



    def load_deps(self):
        self.avatar =avatar.get_by_id(self.avatar_id)
        self.image  =image.get_by_id(self.avatar.image_id)
        self.voice  =voice.get_by_id(self.avatar.voice_id)
        self.account=account.get_by_id(self.voice.account_id)

    def debug(self):
        print("Avatar ID: {0}".format(self.avatar_id))
        print("Text : {0}".format(self.text))
        db.data_describe(self.avatar)
        db.data_describe(self.image)
        db.data_describe(self.voice)
        db.data_describe(self.account)


    def dub_video(self):
        #video_path, audio_path, output_path
        #os.path.join(self.video.path,self.video.name)
        # Get the duration of the audio file
        audio_duration = self.audio.length
        self.video=video.get_closest_videos_by_length(self.audio.link_id,self.avatar_id,self.audio.length)
        if self.video==None:
            print("No video found this length")
            return
        else:
            print("Video found")
        
        video_path=os.path.join(settings.video_directory,self.video.name)
        audio_path=os.path.join(settings.audio_directory,self.audio.name)
        print(audio_path)
        print(self.audio.name)

        output_path=os.path.join(os.path.dirname(settings.video_directory),str(uuid.uuid4())+".mp4")
        # Get the duration of the video file
        video_duration =self.video.length

        if audio_duration < video_duration:
            # Trim video if it is longer than the audio
            trim_cmd = ['ffmpeg', '-i', video_path, '-i', audio_path,  '-shortest', '-map', '0:v', '-map', '1:a','-y', output_path]
            subprocess.run(trim_cmd)
        else:
            # Loop video if it is shorter than the audio
            loop_cmd = [ 'ffmpeg' , '-stream_loop', '-1', '-i', video_path ,'-i', audio_path, '-shortest', '-map', '0:v:0', '-map', '1:a:0','-y', output_path]
            subprocess.run(loop_cmd)

        self.video_file=output_path
        print ("Audio dub done")        


def process(avatar_id,text):
    # link is the owner of the utterance
    # avatar is the speaker of the utterance
    # text is the content of the utterance
    utterance_obj=utterance_builder(avatar_id,text)
    


def process_batch(avatar_id,file_path):
    # link is the owner of the utterance
    # avatar is the speaker of the utterance
    # text is the content of the utterance

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            # Process each line

            print("Processing: {0}".format(line.strip()))
            utterance_obj=utterance_builder(avatar_id,line.strip())

