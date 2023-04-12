import json
import threading

import openai

from pypetto.resources.gpt_prompt import *
from pypetto.modules.token_stream_parser import TokenStreamParser


class GPTClient:

    def __init__(self, api_key):

        # OpenAI API
        openai.api_key = api_key

        # Query parameters
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 3000
        self.temperature = 0.05
        self.frequency_penalty = 0
        self.presence_penalty = 0

        # streaming in background
        self._stream_reader_thread = None
        self._stream_token_parser = None

    def query_claims_questions(self, text):

        # GPT request
        response = self._build_claims_questions_request(text, PROMPT_OUTPUT_QUERY, stream=False)

        # return parse response
        return self._parse_full_json_response(response)

    def stream_claims_questions(self, text):

        # GPT request
        response = self._build_claims_questions_request(text, PROMPT_OUTPUT_STREAM, stream=True)

        # init token stream parser
        self._stream_token_parser = TokenStreamParser(item_key_re=PROMPT_OUTPUT_STREAM_REGEX, item_stop_char='{')

        # start reader thread
        self._stream_reader_thread = threading.Thread(target=self._stream_reader_thread_func, args=(response,))
        self._stream_reader_thread.start()

        # return result generator
        return self._stream_token_parser.output_gen()

    def _stream_reader_thread_func(self, response):

        # iterate response chunks
        for chunk in response:

            # parse chunk
            chunk_data, finish_reason = self._parse_stream_chunk_response(chunk)

            # push new text to parser
            if chunk_data:
                self._stream_token_parser.feed(chunk_data)

        # mark EOS
        self._stream_token_parser.mark_eos()

    def _build_claims_questions_request(self, text, output_prompt, stream: bool):

        # build request
        response = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            messages=[
                {"role": "system", "content": PROMPT_ROLE},
                {"role": "user", "content": PROMPT_ROLE + PROMPT_CLAIMS_QUESTIONS + output_prompt + PROMPT_CLAIMS_QUESTIONS_ENDING},
                {"role": "user", "content": text},
            ],
            stream=stream
        )

        return response

    @staticmethod
    def _parse_full_json_response(chat_completion_response):

        # parse json
        return json.loads(chat_completion_response['choices'][0]['message']['content'])

    @staticmethod
    def _parse_stream_chunk_response(stream_chunk):

        # check if any content arrived
        if 'content' not in stream_chunk['choices'][0]['delta']:
            return None, stream_chunk['choices'][0]['finish_reason']

        # extract content and finish reason
        return stream_chunk['choices'][0]['delta']['content'], stream_chunk['choices'][0]['finish_reason']
