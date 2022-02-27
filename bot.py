import logging
from urllib.parse import quote, urljoin

from decouple import config
from telegram.ext import CommandHandler, Updater

from download import download

logger = logging.getLogger(__name__)


def download_video(update, context):
    for url in context.args:
        data = download(url)
        with open(data["filename"], "rb") as video:
            update.message.reply_video(video, quote=True)


def main(token, debug=False, port=80, webhook_url=""):
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler("download", download_video))

    if debug:
        updater.start_polling()
    else:
        url = urljoin(webhook_url, quote(token))
        print(f"{url=}")

        updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=url,
        )


if __name__ == "__main__":
    kwargs = (
        dict(debug=debug)
        if (debug := config("DEBUG", default=False, cast=bool))
        else dict(
            port=config("PORT", default=80, cast=int),
            webhook_url=config("WEBHOOK_URL"),
        )
    )
    print(f"{kwargs=}")
    main(token=config("TOKEN"), **kwargs)
