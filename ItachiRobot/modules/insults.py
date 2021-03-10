  
import html
import random
import ItachiRobot.modules.insults_string as insults_string
from ItachiRobot import dispatcher
from telegram import ParseMode, Update, Bot
from ItachiRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async

@run_async
def insults(update: Update, context: CallbackContext):
    args = context.args
    update.effective_message.reply_text(random.choice(insults_string.INSULT))

INSULT_HANDLER = DisableAbleCommandHandler("insult", insult)

dispatcher.add_handler(INSULT_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
