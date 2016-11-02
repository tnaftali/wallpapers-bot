import telegram
import unittest
import label


class ProgramTest(unittest.TestCase):
    @staticmethod
    def test_bot():
        token = '287909822:AAFlFrdJudsCbegW8-5K3FIUna_0Ciu23RY'
        bot = telegram.Bot(token=token)
        print(bot.getMe())

    @staticmethod
    def test_labels_dog():
        print label.main('/Users/Toby/Downloads/dog.jpg')
