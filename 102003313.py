import moviepy
import threading *
import youtube_dl *
import os
import sys
import zipfile
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import streamlit as st
import time

flag=0
st.title('Mashup:musical_note::musical_note::musical_note:')
st.write('Made by Radhika')
video_name=st.text_input("Singer Name")
total=int(st.number_input("Number of videos",step=1))
time=int(st.number_input("Duration(in seconds)",step=1))

Email=st.text_input("Email id")
if st.button('Submit'):

   #To download video
   def download_video( total, video_name):
      ydl_opts = {
         'outtmpl': '%(title)s.%(ext)s',
         'format': 'worst[ext=mp4]',
      }
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
         yt_search = f'ytsearch{total}:{video_name}'
         data = ydl.extract_info(yt_search, download="url")
         videos_list = data['entries']
         for i, video in enumerate(videos_list[:total]):
               video_url = video['webpage_url']
               video_file = ydl.prepare_filename(video)
               ydl.download([video_url])
               new_video_file = f"{i+1}.mp4"
               os.rename(video_file, new_video_file)   


   def convert_trim(number, time):
   #Video to Audio
      video = VideoFileClip("%d.mp4"%(number))
      audio = video.audio
      audio.write_audiofile("%d.mp3"%(number))

   #Trim the audio
      audio_clip = AudioFileClip("%d.mp3"%(number))
      trimmed_audio = audio_clip.subclip(0, time)
      trimmed_audio.write_audiofile("Trimed_%d.mp3"%(number))
        
      
   #Calling function to download the video
      download_video(total, video_name)
   #Using multi threading to convert and trim the video to desired lenght audio
      for i in range (total):
         number = i+1
         t = threading.Thread(target=convert_trim, args=(number, time))
         t.start()
      for i in range (total):
         t.join()
   #Concatenation of all the trimed audio files
      files = []
      for i in range(1, number+1):
         files.append("Trimed_" + str(i) + ".mp3")
      all_mp3 = [AudioFileClip(file) for file in files]
      combined_audio = concatenate_audioclips(all_mp3)
      combined_audio.write_audiofile(output)

   def compress_mp3_to_zip(output, zip_file_path):
      with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
         zip_file.write(output)
         compress_mp3_to_zip('output', 'music.zip')
         flag=1

   main()

if(flag==1):
        with open("music.zip", "rb") as fp:
    
            btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="merged.zip",
            mime="application/zip"
            )
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        from email import encoders

        
# Email credentials
        from_email = "raggarwal1_be20@thapar.edu"
        to_email = Email
        password = "ranzfxsbkhjvkwdx"

# Email settings
        subject = "Zip file attached"
        zip_file_path = 'music.zip'

# Create message
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = subject

# Attach zip file
        with open(zip_file_path, "rb") as f:
             part = MIMEBase("application", "octet-stream")
             part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                f"attachment; filename={zip_file_path}")
        message.attach(part)

# Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(from_email, password)
            smtp.sendmail(from_email, to_email, message.as_string())
            st.write('File sent to', Email)
            end=1


      
      
      
      
