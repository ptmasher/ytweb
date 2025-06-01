from flask import Flask, render_template, request, after_this_request, send_file, flash
import os
import yt_dlp


app = Flask(__name__)
app.secret_key = 'yt_downloader_key'

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/download', methods=['post'])
def download_video():
    url = request.form['url']
    if 'list' in url:
        flash('Playlists are not supported')
        return 'Playlists are not supported', 400
    if not url:
        return 'Url cannot be empty', 400
    
    if not os.path.isdir('videos'):
        os.mkdir('videos')

    ydl_opts = {
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', 'video')
        ydl.download([url])

    file_name = f'{video_title}.mp4'
    file_location = os.path.join('videos', file_name)

    return send_file(file_location, mimetype='video/mp4', as_attachment=True)


app.run(host='0.0.0.0', port='5380', debug=True)