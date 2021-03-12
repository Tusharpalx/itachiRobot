import html
import random
import ItachiRobot.modules.insults_string as insults_string
from ItachiRobot import dispatcher
from telegram import ParseMode, Update, Bot
from ItachiRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async

@run_async
def insult(update: Update, context: CallbackContext):
    args = context.args
    await check_and_send(message, choice(INSULT_STRINGS), parse_mode="html")

INSULT_HANDLER = DisableAbleCommandHandler("insult", insult)

dispatcher.add_handler(INSULT_HANDLER)
