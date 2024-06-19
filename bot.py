import logging
import pathlib

from decouple import config
from telegram import MessageEntity, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def download(url: str):
    data = {}

    def hook(p):
        data["filename"] = f'{p["info_dict"]["id"]}.{p["info_dict"]["ext"]}'

    params = {"postprocessor_hooks": [hook], "outtmpl": "%(id)s.%(ext)s"}
    with YoutubeDL(params=params) as ydl:
        data["retcode"] = ydl.download([url])

    return data


async def handler(update: Update, context):
    urls = context.args or update.message.text.split()
    logger.info(urls)
    for url in urls:
        data = download(url)
        logger.debug(f"{data=}")

        with open(data["filename"], "rb") as video:
            await update.message.reply_video(video, quote=True)

        logger.info(f"Removing {data['filename']}...")
        pathlib.Path(data["filename"]).unlink()


def main(token, debug=False, port=80, webhook_url=""):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("download", handler))
    app.add_handler(MessageHandler(filters.Entity(MessageEntity.URL), handler))

    if debug or not webhook_url:
        app.run_polling()
    else:
        url = "/".join([webhook_url.strip("/"), token])
        logger.debug(f"{url=}")
        app.start_webhook(listen="0.0.0.0", port=port, url_path=token, webhook_url=url)


if __name__ == "__main__":
    kwargs = dict(
        debug=config("DEBUG", default=False, cast=bool),
        port=config("PORT", default=3000, cast=int),
        webhook_url=config("WEBHOOK_URL", default=""),
    )
    main(token=config("TOKEN"), **kwargs)
