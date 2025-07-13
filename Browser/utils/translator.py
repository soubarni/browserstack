import requests
import time

class Translator:
    def __init__(self, source_lang='es', target_lang='en', max_retries=3):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.max_retries = max_retries
        self.base_url = "https://api.mymemory.translated.net/get"

    def translate(self, text):
        params = {
            "q": text,
            "langpair": f"{self.source_lang}|{self.target_lang}"
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()['responseData']['translatedText']
            except Exception as e:
                print(f"Translation error (attempt {attempt + 1}): {e}")
                time.sleep(1)
        return text