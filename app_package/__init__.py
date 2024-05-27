from bot import start, send_news_to_all_users, timezone_callback, stop_subscription, bot_description
from config import TELEGRAM_BOT_TOKEN
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import asyncio


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    description_handler = CommandHandler('bot_description', bot_description)
    application.add_handler(description_handler)

    application.add_handler(CallbackQueryHandler(timezone_callback))

    stop_handler = CommandHandler('stop', stop_subscription)
    application.add_handler(stop_handler)

    application.run_polling()


async def main():
    await asyncio.gather(send_news_to_all_users())

asyncio.run(main())
