import os
from typing import List
from unittest import TestCase

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from httpx import AsyncClient

from pypetto.api import app


class TestAPI(TestCase):

    def setUp(self) -> None:

        # load env
        load_dotenv()

        # init api client
        self.api_client = TestClient(app)

    def test_env_vars(self):
        self.assertIn('OPENAI_KEY', os.environ, msg='OpenAI API Key was not found in ENV_VAR="OPENAI_KEY"')
        self.assertIn('GOOGLE_CRED_FILE_PATH', os.environ, msg='Google Credentials File Path was not found in ENV_VAR="GOOGLE_CRED_FILE_PATH"')

    def test_claims(self):

        TEST_TEXT = "GPT stands for Generative Pre-trained Transformer " \
                    "and it refers to a class of language models developed by OpenAI."
        TEST_LANG = "he"

        response = self.api_client.post(
            "/claims",
            json={
                "text": TEST_TEXT,
                "lang": TEST_LANG
            }
        )
        self.assertEqual(response.status_code, 200)

        # get response data
        api_response = response.json()

        # verify structure
        for key in ('claims', 'questions'):
            self.assertIn(key, api_response, msg=f'Key "{key}" should be in response')
            self.assertTrue(isinstance(api_response[key], List), msg=f'Key "{key}" should be a List')
            self.assertLessEqual(1, len(api_response[key]), msg=f'List "{key}" should have at least one item')
            self.assertTrue(all(isinstance(v, str) for v in api_response[key]), msg=f'Items in list "{key}" should be strings')


@pytest.mark.anyio
async def test_root():

    load_dotenv()

    TEST_TEXT = "GPT stands for Generative Pre-trained Transformer " \
                "and it refers to a class of language models developed by OpenAI."
    TEST_LANG = "he"

    async with AsyncClient(app=app, base_url="http://test") as client:
        async with client.stream(
                "POST",
                "/api/claims_stream",
                json={'text': TEST_TEXT, 'lang': TEST_LANG}
        ) as response:
            async for line in response.aiter_lines():
                print(line.strip())
