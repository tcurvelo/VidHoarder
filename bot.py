import logging

from decouple import config
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.messageentity import MessageEntity

from download import download

logger = logging.getLogger(__name__)


def download_video(update, context):
    urls = context.args or update.message.text.split()
    logger.info(urls)
    for url in urls:
        data = download(url)
        with open(data["filename"], "rb") as video:
            update.message.reply_video(video, quote=True)


def main(token, debug=False, port=80, webhook_url=""):
    updater = Updater(token=token)
    for handler in [
        CommandHandler("download", download_video),
        MessageHandler(Filters.entity(MessageEntity.URL), download_video),
    ]:
        updater.dispatcher.add_handler(handler)

    if debug:
        updater.start_polling()
    else:
        url = "/".join([webhook_url.strip("/"), token])
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
