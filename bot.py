from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from FtxClient import FtxClient
import logging
import os

key = os.environ['FTXKEY']
secret = os.environ['FTXSEC']
token = os.environ["TOKEN"]
PORT = int(os.environ.get('PORT', 5000))
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

updater = Updater(token, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /show "Crypto Pair": Shows the current price of Crypto Pair
	""")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def show(update: Update, context: CallbackContext):
    pair = update.message.text[6:]
    ftx = FtxClient(key, secret, 'Main account')
    try:
        dt = ftx.get_single_market(pair)
        update.message.reply_text(
            "Price for pair: '%s'" % dt['price'])
    except:
        update.message.reply_text(
            "No such market at FTX Exchange: '%s'" % pair)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('show', show))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=token)
updater.bot.setWebhook('https://spc-bot.herokuapp.com/' + token)

updater.start_polling()
