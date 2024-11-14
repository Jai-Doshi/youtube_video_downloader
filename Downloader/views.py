from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
import datetime
from model.youtube_video_downloader import YouTubeVideoDownloader


def home(request):
    context = {
        'video_fetched': False,
        'youtube_video': None,
    }

    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        action = request.POST.get('action')

        youtube_video_downloader = YouTubeVideoDownloader(video_url)

        if action == "preview":
            # Fetch video details only
            yt, _ = youtube_video_downloader.download_video(fetch_only=True)
            if yt:
                context.update({
                    'video_fetched': True,
                    'title': yt.title,
                    'thumbnail': yt.thumbnail_url,
                    'duration': str(datetime.timedelta(seconds=yt.length)),
                    'youtube_video': video_url,
                })
                messages.success(request, 'Your video has been fetched !')
            else:
                # context['error'] = "Unable to fetch video details. Please check the URL."
                messages.error(request, 'Unable to fetch video details. Please check the URL.')

        elif action == "download":
            # Download the video to MEDIA_ROOT
            yt, video_stream = youtube_video_downloader.download_video(fetch_only=False)
            if yt and video_stream:
                video_stream.download(output_path=settings.MEDIA_ROOT)
                context.update({
                    'video_fetched': True,
                    'title': yt.title,
                    'thumbnail': yt.thumbnail_url,
                    'duration': str(datetime.timedelta(seconds=yt.length)),
                    'youtube_video': video_url,
                    'downloaded': True,
                })
                messages.success(request, 'Your video has been downloaded !')
            else:
                # context['error'] = "Failed to download the video. Please try again."
                messages.error(request, 'Failed to download the video. Please try again.')

    return render(request, 'home.html', context)