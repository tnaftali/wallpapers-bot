import logging, cloudinary, cloudinary.api
from telegram import InlineQueryResultPhoto
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from random import shuffle

cloudinary.config(
    cloud_name='dmyufekev',
    api_key='166958157613447',
    api_secret='086xPNR_jROA04gcDSdRnqxf2iE'
)

token = '287909822:AAGnrEfRDaVLuqM-IqKqW-Ph1os2rdLXZoE'
updater = Updater(token=token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    text = 'This Bot helps you find wallpapers that you like. \n \n' \
           'You can search by tag typing "@mobilewallpapersbot" followed by a word, and it ' \
           'will search images tagged with that word. \n' \
           'You can also use the /tags command to get five random tags, or /random to get a random wallpaper. \n' \
           'This bot uses the Google Cloud Vision API to tag the images.'
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def get_images_inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    tag = str(query)
    response = cloudinary.api.resources_by_tag(tag)
    photos = response['resources']
    if photos is None or len(photos) == 0:
        bot.answerInlineQuery(update.inline_query.id, results)
    results = list()
    for i in range(len(photos)):
        photo = photos[i]['secure_url']
        thumb = create_thumb(photo)
        results.append(
            InlineQueryResultPhoto(
                id=i,
                photo_height=100,
                photo_width=100,
                photo_url=photo,
                thumb_url=thumb
            )
        )
    if len(results) > 0:
        bot.answerInlineQuery(update.inline_query.id, results)


def create_thumb(photo):
    arr = photo.split('/upload/')
    two = arr[1].split('/')[1]
    one = arr[0] + '/upload/q_30/'
    return str(one) + str(two)


def get_tags(bot, update):
    max = 500
    count = 5
    text = ''
    response = cloudinary.api.tags(max_results=max)
    tags = response['tags']
    shuffle(tags)
    for i in range(count):
        text += tags[i] + '\n'
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=text)


def get_random(bot, update):
    max = 500
    response = cloudinary.api.resources(max_results=max)
    photos = response['resources']
    shuffle(photos)
    photo = photos[0]['secure_url']
    bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)


def help(bot, update):
    text = 'You can search by tag typing "@mobilewallpapersbot" followed by a word, and it ' \
           'will search images tagged with that word. \n \n' \
           'You can also use the /tags command to get five random tags, or /random to get a random wallpaper. \n'
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=text)


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

tags_handler = CommandHandler('tags', get_tags)
dispatcher.add_handler(tags_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

random_handler = CommandHandler('random', get_random)
dispatcher.add_handler(random_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

dispatcher.add_error_handler(error_callback)

updater.start_polling()
updater.idle()
