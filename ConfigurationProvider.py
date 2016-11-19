from ConfigurationHelper import ConfigurationHelper


class ConfigurationProvider:
    def __init__(self):
        config_helper = ConfigurationHelper()
        config = config_helper.config_section_map('Config')
        self.token = config.get('dev_token')
        self.image_tag = config.get('image_tag')
        self.telegram_max = int(config.get('telegram_max'))
        self.not_found_image = config.get('not_found_image')
        self.image_types = config.get('image_types')
        self.review_tag = config.get('review_tag')
        self.max = int(config.get('cloudinary_max'))
        self.cloud_name = config.get('cloud_name')
        self.api_key = config.get('api_key')
        self.api_secret = config.get('api_secret')

