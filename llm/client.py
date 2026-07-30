from openai import OpenAI
from config import BASE_URL, API_KEY


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    @property
    def chat(self):
        return self.client.chat.completions
