from bot import start, send_news_to_all_users, timezone_callback
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

    application.add_handler(CallbackQueryHandler(timezone_callback))

    application.run_polling()


async def main():
    await asyncio.gather(start(), send_news_to_all_users())

asyncio.run(main())
