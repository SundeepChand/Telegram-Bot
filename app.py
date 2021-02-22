import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from flask import Flask, request

from utils import get_reply, fetch_news, topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1628353696:AAH-bddmfD4BtqotsSmVys6Tf1j_h6ZQyRU'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello!'

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"

def start(update, context):
    author = update.message.from_user.first_name
    reply = f'Hi! {author}'
    print(reply)
    update.message.reply_text(reply)

def _help(update, context):
    help_txt = "Hi I'm Newsy, your news fetching bot. Just type the kind of news you want & I'll fetch it for you."
    update.message.reply_text(help_txt)

def news(update, context):
    bot.send_message(chat_id=update.message.chat.id, text='Choose a category', 
        reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))

def reply_text(update, context):
    intent, reply = get_reply(update.message.text, update.message.chat.id)
    print(reply)
    if intent == 'get_news':
        update.message.reply_text('Just a second, fetching some awesome news for you')
        news_articles = fetch_news(reply)
        if len(news_articles) == 0:
            update.message.reply_text('Uh oh! Could not find any news at the moment. Try a different category.')
            return
        for article in news_articles:
            update.message.reply_text(article['link'])
    else:
        update.message.reply_text(reply)

def echo_sticker(update, context):
    print(update.message)
    update.message.reply_sticker(update.message.sticker.file_id)

def error(bot, update):
    logger.error(f'Update {update} caused error {update.error}.')

bot = Bot(TOKEN)
try:
    bot.set_webhook('https://protected-reaches-77087.herokuapp.com/' + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)

if __name__ == '__main__':
    app.run(port=8443)