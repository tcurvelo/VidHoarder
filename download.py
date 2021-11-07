import mimetypes

from youtube_dl import YoutubeDL


def download(url: str):
    def hook(progress):
        if progress.get("status") == "finished":
            data["filename"] = progress.get("filename")
            data["media_type"] = mimetypes.guess_type(data["filename"])[0]

    data = {}
    with YoutubeDL(params={"progress_hooks": [hook]}) as ydl:
        data["retcode"] = ydl.download([url])

    return data
