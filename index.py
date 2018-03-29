from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
from pytube.extract import video_id
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<link>')
def downloading_func(link):
    link="https://www.youtube.com/watch?v="+link
    yt=YouTube(link)
    dict={}
    dict['link']=link
    dict['thumbnail_url']=yt.thumbnail_url
    dict['title']=yt.title
    dict['720p']= False if not yt.streams.filter(res="720p",file_extension="mp4",progressive=True).all() else True
    dict['360p']= False if not yt.streams.filter(res="360p",file_extension="mp4",progressive=True).all() else True
    dict['audio']= False if not yt.streams.filter(only_audio=True,subtype="mp4").all() else True
    return render_template('download.html',dict=dict)

@app.route('/intermediate', methods=["POST"])
def download_func():
    if request.method == "POST":
        link=video_id(request.form["url"])
        return redirect(url_for('downloading_func',link=link))

@app.route('/downloading', methods=["POST"])
def download_now():
    if request.method=="POST":
        yt=YouTube(request.form["url"])
        if request.form["quality"]=="720p":
            yt.streams.filter(res="720p",file_extension="mp4",progressive=True).first().download()
        elif request.form["quality"]=="360p":
            yt.streams.filter(res="360p",file_extension="mp4",progressive=True).first().download()
        elif request.form["quality"]=="Audio Only":
            yt.streams.filter(only_audio=True,subtype="mp4").first().download()
        else:
             return "Failure"
        return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug = True)