import mimetypes

from yt_dlp import YoutubeDL

def download(url: str):
    def hook(progress):
        if progress["status"] == "finished":
            data["filename"] = f'{progress["info_dict"]["id"]}.{progress["info_dict"]["ext"]}'
            data["media_type"] = mimetypes.guess_type(data["filename"])[0]

    data = {}
    with YoutubeDL(
        params={
            "postprocessor_hooks": [hook],
            "outtmpl": "%(id)s.%(ext)s"
        }
    ) as ydl:
        data["retcode"] = ydl.download([url])

    return data


if __name__ == "__main__":
    import sys

    print(download(sys.argv[1]))
