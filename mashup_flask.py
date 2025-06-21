# ©2023 JASHAN WALIA Pvt Ltd. ALL RIGHTS RESERVED
import threading
from pytube import YouTube
import requests
import re
from moviepy.editor import *
import zipfile

#To download video
def download_video( total, video_name):
   search_query =video_name
   search_url = f"https://www.youtube.com/results?search_query={search_query}"
   results_page = requests.get(search_url)
   video_ids = re.findall(r"watch\?v=(\S{11})", results_page.text)
   video_links = [f"https://www.youtube.com/watch?v={id}" for id in video_ids]
   for i in range (total):
      video = YouTube(video_links[i])
      audio = video.streams.filter(only_audio=False).first()
      audio.download(filename="%d.mp4"%(i+1))  
      print("Video " + str(i+1) + "downloaded")  

def convert_trim(number, time):
#Video to Audio
   video = VideoFileClip("%d.mp4"%(number))
   audio = video.audio
   audio.write_audiofile("%d.mp3"%(number))
#Trim the audio
   audio_clip = AudioFileClip("%d.mp3"%(number))
   trimmed_audio = audio_clip.subclip(0, time)
   trimmed_audio.write_audiofile("Trimed_%d.mp3"%(number))

def main(singer, num_videos, duration):    
   total = num_videos
   video_name = singer
   time = duration
#Calling function to download the video
   download_video(total, video_name)
#Using multi threading to convert and trim the video to desired lenght audio
   threads = []
   for i in range (1, total+1):
      t = threading.Thread(target=convert_trim, args=(i, time))
      threads.append(t)
      t.start()
   for t in threads:
      t.join()
#Concatenation of all the trimed audio files
   files = []
   for i in range(1, total+1):
      files.append("Trimed_" + str(i) + ".mp3")
   all_mp3 = [AudioFileClip(file) for file in files]
   combined_audio = concatenate_audioclips(all_mp3)
   combined_audio.write_audiofile("combined.mp3")
   #Zip file conversion
   with zipfile.ZipFile('combined.zip', 'w') as zip:
      zip.write('combined.mp3')