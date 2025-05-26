from flask import Flask, render_template, request, flash
from os import chdir
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/download', methods=['post'])
def download_video():
    url = request.form['url']
    if not url:
        return None
    
    title = '%(title)s.%(ext)s'

    ydl_opts = {
        'outtmpl': title,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        chdir('./videos')
        ydl.download([url])
        return flash('Video saved in "videos" folder')


app.run(host='0.0.0.0', port='5380')