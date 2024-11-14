from pytubefix import YouTube
from pytubefix.cli import on_progress

class YouTubeVideoDownloader:
    def __init__(self, video_url):
        self.video_url = video_url

    def download_video(self, fetch_only=False):
        try:
            yt = YouTube(self.video_url, on_progress_callback=on_progress)
            video_stream = yt.streams.get_highest_resolution()
            if fetch_only:
                return yt, None
            return yt, video_stream
        except Exception as e:
            error = f'Error: {e}'
            return error, None
