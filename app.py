from flask import Flask, request, render_template, redirect
import smtplib  #Simple mail transfer propocal
from flask_mail import Mail, Message
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from mashup_flask import *
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])  
def rootpage():
   singer=''
   num_videos=''
   duration=''
   email=''
   if request.method =='POST' :
      singer = request.form.get('singer_name')
      num_videos = int(request.form.get('num_videos'))
      duration = int(request.form.get('duration'))
      email  = request.form.get('email') 
      singer = singer.lower()
   
      main(singer, num_videos, duration)
      # MAIL
      msg = MIMEMultipart()
      msg['From'] = 'test.mail160122@gmail.com'
      msg['To'] = COMMASPACE.join(email)
      msg['Subject'] = 'Result zip file'
      
      with open('combined.zip', 'rb') as f:
         part = MIMEApplication(f.read(), Name='combined.zip')
         part['Content-Disposition'] = 'attachment; filename="combined.zip"'
         msg.attach(part)
      
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login("test.mail160122@gmail.com", "rwuugkeignpxkljm")
      server.sendmail("test.mail160122@gmail.com", email, msg.as_string())
   return render_template("index.html", 
                       singer=singer,
                       num_videos=num_videos,
                       duration=duration,
                       email=email) 
      
app.run()
