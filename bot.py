import logging, cloudinary, cloudinary.api
from telegram import InlineQueryResultPhoto
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from random import shuffle
import flask

app = flask.Flask(__name__)

@app.route("/")

cloudinary.config(
    cloud_name='dmyufekev',
    api_key='166958157613447',
    api_secret='086xPNR_jROA04gcDSdRnqxf2iE'
)

token = '287909822:AAFlFrdJudsCbegW8-5K3FIUna_0Ciu23RY'
updater = Updater(token=token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def get_images_inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    tag = str(query)
    response = cloudinary.api.resources_by_tag(tag)
    photos = response['resources']
    results = list()
    for i in range(len(photos)):
        photo = photos[i]['secure_url']
        print photo
        results.append(
            InlineQueryResultPhoto(
                id=i,
                photo_url=photo,
                thumb_url=photo
            )
        )
    if len(results) > 0:
        bot.answerInlineQuery(update.inline_query.id, results)


def get_tags(bot, update, args):
    count = 0
    text = ''
    if not None and not '':
        try:
            count = int(' '.join(args))
        except:
            text = 'Please specify how many tags you want to get'
        response = cloudinary.api.tags(max_results=count)
        tags = response['tags']
        shuffle(tags)
        for tag in tags:
            text += tag + '\n'
        bot.sendMessage(chat_id=update.message.chat_id,  parse_mode='HTML', text=text)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Sorry, I didn\'t understand that command.')


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        print error
    except BadRequest:
        # handle malformed requests - read more below!
        print error
    except TimedOut:
        # handle slow connection problems
        print error
    except NetworkError:
        # handle other connection problems
        print error
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        print error
    except TelegramError:
        # handle all other telegram related errors
        print error


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

inline_images_handler = InlineQueryHandler(get_images_inline)
dispatcher.add_handler(inline_images_handler)

tags_handler = CommandHandler('tags', get_tags, pass_args=True)
dispatcher.add_handler(tags_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

dispatcher.add_error_handler(error_callback)

updater.start_polling()
updater.idle()
