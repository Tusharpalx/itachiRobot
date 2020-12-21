import html
import random
import ItachiRobot.modules.animequote_string as animequote_string
from ItachiRobot import dispatcher
from telegram import ParseMode, Update, Bot
from ItachiRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async

@run_async
def aq(update: Update, context: CallbackContext):
    args = context.args
    update.effective_message.reply_text(random.choice(animequote_string.ANIMEQUOTE))

AQ_HANDLER = DisableAbleCommandHandler("aq", aq)

dispatcher.add_handler(AQ_HANDLER)
