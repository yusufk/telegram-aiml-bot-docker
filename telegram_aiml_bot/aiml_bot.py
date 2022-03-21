#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

A default handler functions is defined which passes all incoming text messages to the AIML engine.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Configure your Telegram bot parameters in the config.env file.
Copy your AIML files into the AIML directory and start the app.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from xmlrpc.client import boolean
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
import aiml
import os
import time, sys
from functools import wraps
from settings import settings
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

terminate = ['bye','buy','shutdown','exit','quit','gotosleep','goodbye']

#Config
list_of_admins = settings.admins
logger.debug(list_of_admins)
master_id = list_of_admins[0]
logger.debug(master_id)
defcon_level = 5
lastMsg = ""
lastMsgTime = time.time()-300 

# Initiate the aiml engine
kernel = aiml.Kernel()
kernel.setTextEncoding( None )

if os.path.isfile("AIML/standard.brn"):
    logging.info("Loading AIML files from brain file")
    kernel.bootstrap(brainFile = "AIML/standard.brn")
else:
    kernel.bootstrap(learnFiles = "AIML/std-startup.xml", commands = "load aiml b")
    kernel.setBotPredicate("name", "Jarvis")
    kernel.setBotPredicate("botmaster", "@yusufk")
    kernel.saveBrain("AIML/standard.brn")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id not in list_of_admins:
            logging.warn("Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text("Your unauthorised access attempt has been logged...")
            return
        return func(update, context)
    return wrapped

@restricted
def jarvis(update: Update, context: CallbackContext):
    try:
        update.message.reply_text(kernel.respond(update.message.text))
    except:
        logger.error("AIML error:"+ str(sys.exc_info()[0]))

def error(update: Update, context: CallbackContext, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    # Get the environment variables
    token = settings.token
    updater = Updater(token, use_context=True)
    PORT = settings.telegram_callback_port
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # add handlers  
    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(Filters.text, jarvis))
 
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if settings.use_telegram_callback:
        URL = settings.telegram_callback_url
        updater.start_webhook(listen="0.0.0.0",
        port=int(PORT),
        url_path=token,
        webhook_url = URL + token)
    else:
        updater.start_polling()
    
    updater.bot.send_message(chat_id=master_id, text="Good day sir!")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    #updater.idle(stop_signals=(2, 15, 6, 13))
    updater.idle()

if __name__ == '__main__':
    main()