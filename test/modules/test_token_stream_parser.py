import threading
from time import sleep
from unittest import TestCase

from pypetto.modules.token_stream_parser import TokenStreamParser


class TestTokenStreamParser(TestCase):

    TEST_TEXT = '{C#1} GPT is a class of language models developed by OpenAI, based on a deep learning architecture called a transformer and trained on vast amounts of text data using unsupervised learning techniques.' \
                '{C#2} The goal of GPT models is to generate coherent and fluent human-like text, given a prompt or context.' \
                '{C#3} GPT models achieve their goal by predicting the most likely word or sequence of words to follow a given text input, based on the patterns and relationships learned from the training data.' \
                '{Q#1} How is GPT trained and what unsupervised learning techniques are used?' \
                '{Q#2} What is the ultimate goal of GPT models?' \
                '{Q#3} How do GPT models generate coherent and fluent text?' \
                '{Q#4} What patterns and relationships do GPT models use to predict the most likely word or sequence of words to follow a given text input?' \
                '{Q#5} How accurate and reliable are GPT models in generating human-like text?'

    def setUp(self) -> None:

        self.item_prefix_re = r"\{([CQ])#(\d)\}"
        self.item_stop_char = "{"

        self.token_parser = TokenStreamParser(self.item_prefix_re, self.item_stop_char)

    def test_chat_completion(self):

        parsed_response = dict()

        def _process_output_worker(token_parser):

            # consume output generator
            for item_key, text_delta in token_parser.output_gen():

                # create new key
                if item_key not in parsed_response:
                    parsed_response[item_key] = ''

                # append text
                parsed_response[item_key] += text_delta

        # create output reader
        output_worker = threading.Thread(target=_process_output_worker, args=(self.token_parser,))
        output_worker.start()

        # feed text
        for char in self.TEST_TEXT:
            self.token_parser.feed(token=char)
            sleep(0.005)

        # mark end
        self.token_parser.mark_eos()

        # wait for thread
        output_worker.join()

        # compare results
        reconstructed_text = ''.join(
            '{' + k[0] + '#' + k[1] + '} ' + v for k, v in parsed_response.items()
        )
        self.assertEqual(self.TEST_TEXT, reconstructed_text, msg="Reconstructed text should be equal!")
