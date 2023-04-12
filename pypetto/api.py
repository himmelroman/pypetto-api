import os
import json

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pypetto.modules.gpt import GPTClient
from pypetto.modules.translate import GoogleTranslateClient


# FastAPI App
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/claims")
async def query_claims_questions(text: str = Body(), lang: str = Body()):

    # create clients
    gpt_client = GPTClient(api_key=os.environ['OPENAI_KEY'])
    translate_client = GoogleTranslateClient(cred_file_path=os.environ['GOOGLE_CRED_FILE_PATH'])

    # query gpt
    gpt_response = gpt_client.query_claims_questions(text)

    # init response
    response_claims = gpt_response['claims']
    response_questions = gpt_response['questions']

    # translate
    if lang != 'en':
        input_text_list = gpt_response['claims'] + gpt_response['questions']
        translated_list = translate_client.translate_batch(input_list=input_text_list, target_lang=lang)
        response_claims = [res['translatedText'] for res in translated_list[0:len(gpt_response['claims'])]]
        response_questions = [res['translatedText'] for res in translated_list[len(gpt_response['claims']):]]

    return {
        'claims': response_claims,
        'questions': response_questions
    }


@app.post("/api/claims_stream")
async def stream_claims_questions(text: str = Body(embed=True), lang: str = Body(embed=True)):

    # create clients
    gpt_client = GPTClient(api_key=os.environ['OPENAI_KEY'])
    stream_gen = gpt_client.stream_claims_questions(text)

    def response_streamer(stream):

        # consume stream
        for item_key, text_delta in stream:
            yield json.dumps({
                    "type": item_key[0],
                    "index": item_key[1],
                    "text": text_delta
            })

    return StreamingResponse(response_streamer(stream_gen), media_type='text/event-stream')
