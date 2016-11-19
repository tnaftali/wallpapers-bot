class TextProvider:
    start = 'You can start using this bot searching by tag typing "@wallpaperss_bot" followed by a word, and it ' \
           'will search images tagged with that word.\n\nYou can also use the /tags command to get' \
            ' five random tags, or /random to get a random wallpaper.'

    help = 'You can search by tag typing "@wallpaperss_bot" followed by a word, and it ' \
           'will search images tagged with that word.\n\n' \
           'You can also use the /tags command to get five random tags, or /random to get a random wallpaper.'

    unknown = 'Sorry, I didn\'t understand that command. To get help on how to use the bot type the /help command.'

    upload = 'To upload an image to be reviewed and added to the wallpapers collection please send me the image ' \
             'as a file.\nThe maximum permitted size is 5 MB.'

    upload_ok = 'Your image was uploaded successfully!\n\n It will be reviewed to be added to the wallpapers collection'

    upload_type_error = 'The file must be an image (PNG, JPG, JPEG)'

    upload_unknown_error = 'There was an error uploading the image, please try again.'
