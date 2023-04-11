import os

from fastapi import FastAPI, Body

from pypetto.modules.gpt import GPTClient
from pypetto.modules.translate import GoogleTranslateClient

# FastAPI App
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/claims")
async def gen_question_claims(text: str = Body(), lang: str = Body()):

    # create clients
    gpt_client = GPTClient(api_key=os.environ['OPENAI_KEY'])
    translate_client = GoogleTranslateClient(cred_file_path=os.environ['GOOGLE_CRED_FILE_PATH'])

    # query gpt
    gpt_response = gpt_client.query_chat_completion(text)

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
