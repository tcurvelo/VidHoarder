import logging
import pathlib

from decouple import config
from telegram.ext import CommandHandler, MessageHandler, filters
from telegram import MessageEntity, Update
from telegram.ext import ApplicationBuilder, CommandHandler

from download import download

logger = logging.getLogger(__name__)


async def download_video(update: Update, context):
    urls = context.args or update.message.text.split()
    logger.info(urls)
    for url in urls:
        data = download(url)
        with open(data["filename"], "rb") as video:
            await update.message.reply_video(video, quote=True)

        pathlib.Path(data["filename"]).unlink()


def main(token, debug=False, port=80, webhook_url=""):
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("download", download_video))
    application.add_handler(MessageHandler(filters.Entity(MessageEntity.URL), download_video))

    if debug or not webhook_url:
        application.run_polling()
    else:
        url = "/".join([webhook_url.strip("/"), token])
        print(f"{url=}")

        application.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=url
        )


if __name__ == "__main__":
    kwargs = dict(
        debug=config("DEBUG", default=False, cast=bool),
        port=config("PORT", default=3000, cast=int),
        webhook_url=config("WEBHOOK_URL", default=""),
    )
    main(token=config("TOKEN"), **kwargs)
