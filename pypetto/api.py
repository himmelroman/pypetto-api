import os
from typing import Annotated

from fastapi import FastAPI, Body

from pypetto.modules.gpt import GPTClient
from pypetto.modules.translate import GoogleTranslateClient

# FastAPI App
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/claims")
async def gen_question_claims(text: Annotated[str, Body()], lang: Annotated[str, Body()] = 'he'):

    # create clients
    gpt_client = GPTClient(api_key=os.environ['OPENAI_KEY'])
    translate_client = GoogleTranslateClient(cred_file_path=os.environ['GOOGLE_CRED_FILE_PATH'])

    # query gpt
    gpt_response = gpt_client.query_chat_completion(text)

    # translate
    input_text_list = gpt_response['claims'] + gpt_response['questions']
    translated_list = translate_client.translate_batch(input_list=input_text_list, target_lang=lang)
    translated_claims = [res['translatedText'] for res in translated_list[0:len(gpt_response['claims'])]]
    translated_questions = [res['translatedText'] for res in translated_list[len(gpt_response['claims']):]]

    return {
        'en': gpt_response,
        lang: {
            'claims': translated_claims,
            'questions': translated_questions
        }
    }
