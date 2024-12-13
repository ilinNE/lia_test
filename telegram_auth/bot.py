from django.conf import settings
from telegram import Update, Bot
from telegram.ext import Updater, CallbackContext, CommandHandler

from telegram_auth.auth_logic import bound_token_with_user, UserInfo


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
updater = Updater(token=settings.TELEGRAM_BOT_TOKEN)
dp = updater.dispatcher


def create_webhook() -> None:
    bot.set_webhook(url=settings.TELEGRAM_LOGIN_REDIRECT_URL)


def start(update: Update, context: CallbackContext) -> None:
    token = update.message.text.replace("/start ", "")
    if token:
        from_user = update.message.from_user
        user_info = UserInfo(id=from_user.id)
        if from_user.username:
            user_info.username = from_user.username
        if from_user.first_name:
            user_info.first_name = from_user.first_name
        if from_user.last_name:
            user_info.last_name = from_user.last_name
        bound_token_with_user(token, user_info)
        update.message.reply_text("Вы успешно авторизованы!")


dp.add_handler(CommandHandler("start", start))
