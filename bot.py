import logging
import cloudinary
import cloudinary.api
import cloudinary.uploader
from telegram import (InlineQueryResultPhoto, InputTextMessageContent)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from random import shuffle, randint

cloudinary.config(
    cloud_name='dmyufekev',
    api_key='166958157613447',
    api_secret='086xPNR_jROA04gcDSdRnqxf2iE'
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)

prod_token = '247049587:AAFp9TUrYCNj58VuN8lwhnr2qu6u0wCVyK4'
dev_token = '270159638:AAGWwsiZnC8GDnr70hR4xaLuLJ1BmeeXbsY'

token = dev_token
updater = Updater(token=token)
dispatcher = updater.dispatcher
handlers = []
max = 500
telegram_max = 50
image_tag = 'wallpaper_image'
not_found_image = 'http://res.cloudinary.com/dmyufekev/image/upload/v1479347414/resources/not_found.png'
image_types = ['image/jpeg']
review_tag = 'REVIEW'


def start(bot, update):
    text = 'You can start using this bot searching by tag typing "@wallpaperss_bot" followed by a word, and it ' \
           'will search images tagged with that word.\n\n'\
           'You can also use the /tags command to get five random tags, or /random to get a random wallpaper.'
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def get_images_inline(bot, update):
    query = update.inline_query.query
    if not query:
        response = cloudinary.api.resources_by_tag(image_tag, max_results=max)
    else:
        tag = str(query)
        response = cloudinary.api.resources_by_tag(tag, max_results=max)
    photos = response['resources']
    shuffle(photos)
    results = list()
    i = 0
    while i < len(photos) and i < telegram_max:
        photo = photos[i]['secure_url']
        id = photos[i]['public_id']
        thumb = create_thumb(photo)
        results.append(
            InlineQueryResultPhoto(
                id=id,
                photo_url=photo,
                thumb_url=thumb,
                photo_height=100,
                photo_width=100
            )
        )
        i += 1
    if len(results) > 0:
        bot.answerInlineQuery(update.inline_query.id, results)
    else:
        results.append(
            InlineQueryResultPhoto(
                id='123123',
                photo_url=not_found_image,
                thumb_url=not_found_image,
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
    response = cloudinary.api.tags(max_results=max)
    tags = response['tags']
    shuffle(tags)
    for i in range(count):
        text += tags[i] + '\n'
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=text)


def get_random(bot, update):
    response = cloudinary.api.resources_by_tag(image_tag, max_results=max)
    photos = response['resources']
    shuffle(photos)
    photo = photos[0]['secure_url']
    bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)


def help(bot, update):
    text = 'You can search by tag typing "@mobilewallpapersbot" followed by a word, and it ' \
           'will search images tagged with that word.\n\n' \
           'You can also use the /tags command to get five random tags, or /random to get a random wallpaper.'
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=text)


def unknown(bot, update):
    text = 'Sorry, I didn\'t understand that command. To get help on how to use the bot type the /help command.'
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


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
    text = 'Please send me the image you want to upload.\nIn order to work it must be uploaded as file ' \
           'and not as image.\nThe maximum permitted size is 5 MB.'
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def handle_file(bot, update):
    file = update.message.document
    text_ok = 'Your image was uploaded successfully!\n\n It will be reviewed to be added to the wallpapers collection'
    type_error = 'The file must be an image (PNG, JPG, JPEG)'
    upload_error = 'There was an error uploading the image, please try again.'
    if image_types.__contains__(file.mime_type):
        try:
            photo = bot.getFile(file_id=file.file_id)
            id = 'img_' + str(randint(100000, 999999))
            cloudinary.uploader.upload(photo.file_path, public_id=id)
            cloudinary.uploader.add_tag(review_tag, id)
            bot.sendMessage(chat_id=update.message.chat_id, text=text_ok)
        except:
            bot.sendMessage(chat_id=update.message.chat_id, text=type_error)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=upload_error)


def handle_command(bot, update):
    command = update.message.text
    f(command, bot, update)


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
    add_handlers()
    updater.start_polling()


main()
