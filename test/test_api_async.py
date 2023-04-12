import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

from pypetto.api import app


@pytest.mark.anyio
async def test_stream_claims():

    load_dotenv()

    # Texts
    TEST_TEXT = "GPT stands for Generative Pre-trained Transformer " \
                "and it refers to a class of language models developed by OpenAI."
    TEST_LANG = "he"

    async with AsyncClient(app=app, base_url="http://test") as client:
        async with client.stream(
                "POST",
                "/api/claims_stream",
                json={'text': TEST_TEXT, 'lang': TEST_LANG}
        ) as response:

            # iterate responses in stream
            async for res in response.aiter_lines():
                print(res.strip())
