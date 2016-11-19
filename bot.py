import logging
import cloudinary
import cloudinary.api
import cloudinary.uploader
from telegram import (InlineQueryResultPhoto, InputTextMessageContent)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from random import shuffle, randint
from TextProvider import TextProvider
from ConfigurationProvider import ConfigurationProvider
import threading

config = ConfigurationProvider()

updater = Updater(token=config.token)
dispatcher = updater.dispatcher
handlers = []
dict = dict()

cloudinary.config(
    cloud_name=config.cloud_name,
    api_key=config.api_key,
    api_secret=config.api_secret
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=TextProvider.start)


def get_images_inline(bot, update):
    query = update.inline_query.query
    if not query:
        response = cloudinary.api.resources_by_tag(config.image_tag, max_results=config.max)
    else:
        tag = str(query)
        response = cloudinary.api.resources_by_tag(tag, max_results=config.max)
    photos = response['resources']
    shuffle(photos)
    results = list()
    i = 0
    while i < len(photos) and i < config.telegram_max:
        photo = photos[i]['secure_url']
        id = photos[i]['public_id']
        thumb = create_thumb(photo)
        results.append(
            InlineQueryResultPhoto(
                id=id,
                photo_url=photo,
                thumb_url=thumb,
                photo_height=400,
                photo_width=200
            )
        )
        i += 1
    if len(results) > 0:
        bot.answerInlineQuery(update.inline_query.id, results)
    else:
        results.append(
            InlineQueryResultPhoto(
                id='123123',
                photo_url=config.not_found_image,
                thumb_url=config.not_found_image,
                input_message_content=InputTextMessageContent(
                    message_text="There isn't any image containing that tag"
                )
            )
        )
        bot.answerInlineQuery(update.inline_query.id, results)


def create_thumb(photo):
    arr = photo.split('/upload/')
    two = arr[1].split('/')[1]
    one = arr[0] + '/upload/q_30/'
    return str(one) + str(two)


def get_tags(bot, update):
    count = 5
    text = ''
    response = cloudinary.api.tags(max_results=config.max)
    tags = response['tags']
    shuffle(tags)
    for i in range(count):
        text += tags[i] + '\n'
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=text)


def get_random(bot, update):
    response = cloudinary.api.resources_by_tag(config.image_tag, max_results=config.max)
    photos = response['resources']
    shuffle(photos)
    photo = photos[0]['secure_url']
    bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)


def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=TextProvider.help)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=TextProvider.unknown)


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


def upload_image(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=TextProvider.upload)


def handle_file(bot, update):
    file = update.message.document
    if config.image_types.__contains__(file.mime_type):
        try:
            photo = bot.getFile(file_id=file.file_id)
            id = 'img_' + str(randint(100000, 999999))
            cloudinary.uploader.upload(photo.file_path, public_id=id)
            cloudinary.uploader.add_tag(config.review_tag, id)
            bot.sendMessage(chat_id=update.message.chat_id, text=TextProvider.upload_ok)
        except:
            bot.sendMessage(chat_id=update.message.chat_id, text=TextProvider.upload_unknown_error)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=TextProvider.upload_type_error)


def handle_command(bot, update):
    command = update.message.text
    key = (command, update.message.from_user.username)
    map_command(key)
    if not spam(key):
        f(command, bot, update)


def map_command(key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 0


def spam(key):
    return dict[key] > 10


def empty_dictionary():
    dict.clear()
    threading.Timer(60.0, empty_dictionary).start()


def f(command, bot, update):
    if command == '/start':
        start(bot, update)
    elif command == '/tags':
        get_tags(bot, update)
    elif command == '/help':
        help(bot, update)
    elif command == '/random':
        get_random(bot, update)
    elif command == '/submit':
        upload_image(bot, update)


def add_handlers():
    handlers.append(InlineQueryHandler(get_images_inline))
    handlers.append(MessageHandler(Filters.command, handle_command))
    handlers.append(MessageHandler(Filters.document, handle_file))

    for handler in handlers:
        dispatcher.add_handler(handler)


def main():
    empty_dictionary()
    add_handlers()
    updater.start_polling()
    updater.idle()


main()
