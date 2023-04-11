import os
from typing import List
from unittest import TestCase

from dotenv import load_dotenv

from pypetto.modules.gpt import GPTClient


class TestGPT(TestCase):

    TEST_TEXT = 'GPT stands for "Generative Pre-trained Transformer" ' \
                'and it refers to a class of language models developed by OpenAI. ' \
                'These models are based on a deep learning architecture called a transformer ' \
                'and are trained on vast amounts of text data using unsupervised learning techniques. ' \
                'The goal of GPT models is to generate coherent and fluent human-like text, given a prompt or context. ' \
                'They achieve this by predicting the most likely word or sequence of words to follow a given text input,' \
                ' based on the patterns and relationships learned from the training data.'

    def setUp(self) -> None:

        # load env
        load_dotenv()

        self.client = GPTClient(api_key=os.environ['OPENAI_KEY'])

    def test_translate_text(self):

        gpt_response = self.client.query_chat_completion(text=self.TEST_TEXT)
        self.assertIsNotNone(gpt_response)

        # assert response structure
        for key in ('claims', 'questions'):

            self.assertIn(key, gpt_response, msg="Key should be in response")
            self.assertTrue(isinstance(gpt_response[key], List), msg="Key should contain a list")
            self.assertLessEqual(1, len(gpt_response[key]), msg="List should have at least one item")
            self.assertTrue(all(isinstance(v, str) for v in gpt_response[key]), msg="Items in the list should be strings")
