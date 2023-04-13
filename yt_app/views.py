from django.shortcuts import render, redirect, HttpResponse
from pytube import YouTube
import os
from django.contrib import messages
from wsgiref.util import FileWrapper

# Create your views here.

def index(request):
    return render(request, 'yt_app/index.html')

def getVideo(request):
    if request.method == "POST":
        try:
            url = request.POST.get('url')
            yt = YouTube(url)
            videos = []
            audios = []
            video_only = yt.streams.filter(progressive=True)
            audio_only = yt.streams.filter(abr='128kbps', only_audio=True)
            if video_only:
                for i in video_only:
                    vid_size = round(i.filesize/1024/1024, 1)
                    videos.append([i, vid_size])
            if audio_only:
                audios.append(audio_only[0])
                audios.append(round(audio_only[0].filesize/1024/1024, 1))
            context = {'videos': videos, 'audios': audios, 'thumbnail': yt.thumbnail_url, 'title': yt.title, 'url': url}
            return render(request, 'yt_app/download.html', context)

        except Exception as e:
            messages.warning(request, "Not found! Please check the URL(Link)")
            return redirect("/")

def downloadVid(request):
    if request.method == "POST":
        url = request.POST.get('url')
        itag = request.POST.get('itag')

        yt = YouTube(url).streams.get_by_itag(itag)
        title = yt.title

        homedir = os.path.expanduser("~")
        dirs = os.path.join(homedir, 'Downloads')

        if yt.type != 'audio':
            yt.download(output_path=dirs, filename=f"{title}.mp4")
            file_path = os.path.join(dirs, f"{title}.mp4")
            file = FileWrapper(open(file_path, 'rb'))
            response = HttpResponse(file, content_type='application/vnd.mp4')
            response['Content-Disposition'] = f'attachment; filename = "{title}.mp4"'
            os.remove(file_path)
            return response

        else:
            yt.download(output_path=dirs, filename=f"{yt.title}.mp3")
            file_path = os.path.join(dirs, f"{title}.mp3")
            file = FileWrapper(open(file_path, 'rb'))
            response = HttpResponse(file, content_type='application/audio.mp3')
            response['Content-Disposition'] = f'attachment; filename = "{title}.mp3"'
            os.remove(file_path)
            return response
