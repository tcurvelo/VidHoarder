from decouple import config
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from download import download


def download_video(update, context):
    for url in context.args:
        data = download(url)
        with open(data["filename"], "rb") as video:
            update.message.reply_video(video, quote=True)


def main(token, debug=False, port=80, webhook_url=""):

    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler("download", download_video))
    updater.dispatcher.add_handler(InlineQueryHandler(download_video))

    if debug:
        updater.start_polling()
    else:
        updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=f"{webhook_url}/{token}",
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
    main(token=config("TOKEN"), **kwargs)
