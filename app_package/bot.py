from config import TELEGRAM_BOT_TOKEN
from specific_timezones import specific_timezones
from bot_description import description
from newsapi import fetch_news
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz


bot = Bot(token=TELEGRAM_BOT_TOKEN)
users = set()
scheduler = AsyncIOScheduler()
user_timezones = {}
available_timezones = specific_timezones


async def start(update: Update, context: CallbackContext):
    """Starts the bot and prompts the user to select a timezone"""
    user_id = update.message.from_user.id
    users.add(user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I will send you daily news updates')
    keyboard = [[InlineKeyboardButton(tz, callback_data=tz)] for tz in available_timezones.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Select your timezone:',
                                   reply_markup=reply_markup)

    context.user_data['user_id'] = user_id


async def timezone_callback(update: Update, context: CallbackContext):
    """Callback function to handle timezone selection"""
    user_id = context.user_data.get('user_id')
    if user_id:
        chosen_timezone = update.callback_query.data
        user_timezones[user_id] = available_timezones[chosen_timezone]
        await initialize_scheduler(user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Timezone set successfully')


async def initialize_scheduler(user_id):
    """Initializes the scheduler after the /start command is triggered"""
    if not scheduler.running:
        scheduler.start()
    if user_id in user_timezones:
        chosen_timezone_key = user_timezones[user_id]
        if chosen_timezone_key in specific_timezones.values():
            tz = pytz.timezone(chosen_timezone_key)
            scheduler.add_job(send_news_to_all_users, 'cron', hour=9, minute=0, timezone=tz)
            scheduler.add_job(send_news_to_all_users, 'cron', hour=21, minute=0, timezone=tz)
        else:
            print(f"Error: Chosen timezone key '{chosen_timezone_key}' not found in specific_timezones")


async def send_news_to_all_users():
    """Send news to all users. This is an asynchronous function."""
    news_list = fetch_news()
    for user_id in users:
        if news_list:
            for news in news_list:
                await bot.send_message(chat_id=user_id, text=news)
        else:
            await bot.send_message(chat_id=user_id, text='No news available at the moment')


async def bot_description(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=description)


async def stop_subscription(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    users.discard(user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Subscription has been cancelled successfully')
