import re
from time import sleep


class TokenStreamParser:

    def __init__(self, item_key_re, item_stop_char):

        # parsed items
        self._items = dict()

        # parsing logic
        self._item_stop_char = item_stop_char
        self._item_key_re = re.compile(item_key_re)

        # working buffer
        self._stream_buffer = ''
        self._steam_ended = False

    def feed(self, token):

        # add token to buffer
        self._stream_buffer += token

        # find item keys
        for match in self._item_key_re.finditer(self._stream_buffer):

            # parse item key
            item_key = (match.groups()[0], match.groups()[1])

            # check if new
            if item_key not in self._items:
                self._items[item_key] = {
                    'key_index': match.span()[0],
                    'text_index': match.span()[1]
                }

        for item_key in self._items.keys():

            # get item text
            item_text = self._stream_buffer[self._items[item_key]['text_index']:]

            # slice by stop char
            if item_text.find(self._item_stop_char) != -1:
                item_text = item_text[:item_text.find(self._item_stop_char)]

            # clean
            item_text = item_text.strip()

            # update item text
            self._items[item_key]['text'] = item_text

    def mark_eos(self):
        self._steam_ended = True

    def output_gen(self):

        # iterate as long as not marked ended
        while not self._steam_ended or not self._output_finished():

            # iterate items
            for item_key in sorted(self._items.keys()):

                # get output end
                output_end_index = self._items[item_key].get('output_end_index', 0)

                # get item's current text
                item_text = self._items[item_key].get('text')
                if item_text:

                    # slice delta
                    text_delta = self._items[item_key]['text'][output_end_index:]
                    if text_delta:

                        # update output end index
                        self._items[item_key]['output_end_index'] = self._items[item_key].get('output_end_index', 0) + len(text_delta)

                        yield item_key, text_delta

            sleep(0.001)

    def _output_finished(self):
        return all(len(i['text']) == i.get('output_end_index', 0) for i in self._items.values())
