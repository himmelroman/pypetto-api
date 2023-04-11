import json
import openai

CLAIMS_PROMPT = \
    "You are an assistant for analytical and critical thinking, helping people to detect and challenge populism.\n" \
    "Your task is to extract the main claims made in the text, and generate 5 questions based on these claims.\n" \
    "The questions should demand details of plans and decisions that stem from the claims.\n" \
    "Output only JSON, an object with two lists, one list with the claims named \"claims\" and one with the questions named \"questions\".\n" \
    "Consider the following text:\n{}\n"


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

    def query_chat_completion(self, text):

        # build request
        completion = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            messages=[
                {"role": "system", "content": "You are an assistant for critical thinking."},
                {"role": "user", "content": CLAIMS_PROMPT},
                {"role": "user", "content": text},
            ]
        )

        return json.loads(completion['choices'][0]['message']['content'])
