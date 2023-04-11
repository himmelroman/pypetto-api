import os
from unittest import TestCase

from dotenv import load_dotenv

from pypetto.modules.translate import GoogleTranslateClient


class TestTranslate(TestCase):

    def setUp(self) -> None:

        # load env
        load_dotenv()

        self.client = GoogleTranslateClient(cred_file_path=os.environ['GOOGLE_CRED_FILE_PATH'])

    def test_translate_text(self):

        translated_text = self.client.translate_text(input_text='שלום', target_lang='en')
        self.assertEqual('Hello', translated_text)

    def test_translate_batch(self):

        input_text_list = [
            'שלום',
            'להתראות'
        ]

        translated_list = self.client.translate_batch(input_list=input_text_list, target_lang='en')

        self.assertEqual('Hello', translated_list[0]['translatedText'])
        self.assertEqual('Goodbye', translated_list[1]['translatedText'])
